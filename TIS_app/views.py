from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Page, Paginator
from django.db.models import Model
from django.db.models.aggregates import Max
from django.forms import BaseModelFormSet, Select, modelformset_factory
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from project.settings import INVENTORY_PAGINATE_BY, TREE_PAGINATE_BY
from TIS_app.forms import (
    CircuitForm,
    CommentTreeForm,
    InventoryForm,
    InventoryUpdateForm,
    PhotoTreeForm,
    RegisterForm,
    TreeForm,
)
from TIS_app.models import (
    Circuit,
    Inventory,
    ManagementTree,
    Photo,
    Tree,
    TreeComment,
    ValorizationTree,
)
from TIS_app.permissions import IsOwnerInventoryForObj, IsOwnerOrReadOnly
from TIS_app.serializers import (
    CommentTreeSerializer,
    InventorySerializer,
    PhotoTreeSerializer,
)

# API views --------------------------------------------


class DetailInventoryAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]


class AddPhotoTreeAPIView(CreateAPIView):
    queryset = Photo.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    media_type = "image/*"
    serializer_class = PhotoTreeSerializer

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(many=True, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        id_tree = request.POST.get("tree")
        images = request.FILES.getlist("image")
        data = [{"image": image, "tree": id_tree} for image in images]
        serializer = self.serializer_class(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentTreeAPIView(ListCreateAPIView):
    queryset = TreeComment.objects.all()
    serializer_class = CommentTreeSerializer
    permission_classes = [IsOwnerInventoryForObj]

    def get_queryset(self):
        start = int(self.request.GET.get("start") or 0)
        end = int(self.request.GET.get("end") or start + 10)
        tree = get_object_or_404(Tree, pk=self.request.GET.get("pk"))
        return TreeComment.objects.filter(tree=tree).order_by("-created")[start:end]


# App views ---------------------------------------------


class IndexView(View):
    template_name = "TIS_app/welcome_site.html"
    context: dict[str, Any] = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_inventories = Inventory.objects.filter(author=request.user)
            self.context["inventories_count"] = user_inventories.count()
            self.context["trees_count"] = 0
            for inventory in user_inventories:
                self.context["trees_count"] += inventory.tree_set.all().count()
        return render(request, self.template_name, self.context)


class RegisterView(CreateView):
    model = get_user_model()
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        form.save()
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())


class AllInventoryView(LoginRequiredMixin, ListView):
    model = Inventory
    paginate_by = INVENTORY_PAGINATE_BY

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user).order_by("pk")


class CreateNewInventoryView(LoginRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    success_url = reverse_lazy("index")

    def form_valid(self, form: InventoryForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        try:
            return reverse_lazy("inventory-details", args=[self.object.pk])
        except Exception:
            return super().get_success_url()


class UpdateInventoryView(LoginRequiredMixin, UpdateView):
    model = Inventory
    template_name = "TIS_app/inventory_detail.html"
    form_class = InventoryUpdateForm
    success_url = reverse_lazy("inventory-details")
    paginate_by = TREE_PAGINATE_BY

    def get_page_object(self) -> Page:
        """Get page object, default is returned last page"""
        tree_list = Tree.objects.filter(inventory=self.get_object()).order_by("lp")
        paginator = Paginator(tree_list, self.paginate_by, 0, True)
        return paginator.page(self.request.GET.get("page", paginator.num_pages))

    def get_modelformsets(self, page_obj: Page) -> dict[str, BaseModelFormSet]:
        """
        Return: Dictionary where keys are also formsets prefixes and values are formsets models.
        """
        return {
            "valorization": modelformset_factory(
                model=ValorizationTree,
                fields=(
                    "is_biocenotic",
                    "value",
                ),
                extra=len(page_obj),
                widgets={
                    "is_biocenotic": Select(choices=[(False, "No"), (True, "Yes")])
                },
            ),
            "management": modelformset_factory(
                model=ManagementTree,
                fields=("procedure",),
                extra=len(page_obj),
            ),
        }

    def get_formsets(self, page_obj: Page) -> list[BaseModelFormSet]:
        """
        Return: List of formsets based on models from `get_modelformsets` method.
        """
        modelformsets = self.get_modelformsets(page_obj)

        valorization_formset = modelformsets["valorization"](
            queryset=ValorizationTree.objects.none(),
            initial=[
                {
                    "is_biocenotic": tree.valorizationtree.is_biocenotic,
                    "value": tree.valorizationtree.value,
                }
                for tree in page_obj
                if hasattr(tree, "valorizationtree")
            ],
            prefix="valorization",
        )
        management_formset = modelformsets["management"](
            queryset=ManagementTree.objects.none(),
            initial=[
                {"procedure": tree.managementtree.procedure}
                for tree in page_obj
                if hasattr(tree, "managementtree")
            ],
            prefix="management",
        )
        return [valorization_formset, management_formset]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_obj = self.get_page_object()

        context["page_obj"] = page_obj
        context["is_paginated"] = context["page_obj"].has_other_pages()
        context["formsets"] = self.get_formsets(page_obj)
        context["trees"] = zip(
            page_obj,
            *context["formsets"],
        )
        context["photo_form"] = PhotoTreeForm()
        context["comment_form"] = CommentTreeForm()
        return context

    def get_success_url(self) -> str:
        try:
            if (page := self.request.GET.get("page")) is not None:
                return (
                    reverse_lazy("inventory-details", args=[self.object.pk])
                    + "?page="
                    + page
                )
            return reverse_lazy("inventory-details", args=[self.object.pk])
        except Exception:
            return super().get_success_url()

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # for update inventory
        if "update-inventory" in request.POST:
            form = self.get_form_class()(request.POST, instance=self.get_object())
            # check if form is valid and add message to storage
            if form.is_valid():
                if form.has_changed():
                    messages.success(
                        request, "The inventory has been successfully updated."
                    )
            else:
                messages.error(
                    request, "Something went wrong! The inventory has not been updated."
                )
                for field in form:
                    for err in field.errors:
                        messages.error(request, f"{field.name.upper()}: {err}")
            return super().post(request, *args, **kwargs)
        # for sending formsets, create or update ValorizationTree or ManagementTree objects
        # get inventory and page object
        self.object = self.get_object()
        page_obj = self.get_page_object()
        # set variables
        formsets: dict[str, BaseModelFormSet] = self.get_modelformsets(page_obj)
        models: dict[str, Model] = {
            "valorization": ValorizationTree,
            "management": ManagementTree,
        }
        defaults: dict[str, list] = {
            "valorization": [
                ("is_biocenotic", False),
                ("value", 5),
            ],
            "management": [
                ("procedure", 0),
            ],
        }
        # iteration over formsets
        for key in formsets:
            if key in request.POST:
                # get formset
                formset = formsets[key](
                    request.POST,
                    prefix=key,
                    initial=[
                        {field[0]: getattr(model, field[0]) for field in defaults[key]}
                        for tree in page_obj
                        if (model := getattr(tree, key + "tree", False))
                    ],
                )
                # check if formset is valid
                if formset.is_valid():
                    for form, tree in zip(formset, page_obj):
                        # get or create object
                        obj, _ = models[key].objects.get_or_create(tree=tree)
                        # check if form has changed
                        if form.has_changed():
                            # overwrite attribute object
                            for field in defaults[key]:
                                value = form.cleaned_data.get(field[0], field[1])
                                setattr(obj, field[0], value)
                                obj.save()

        return HttpResponseRedirect(self.get_success_url())


class AddTreeToInventoryView(LoginRequiredMixin, CreateView):
    model = Tree
    form_class = TreeForm
    success_url = reverse_lazy("inventory-details")
    initial: dict[str, Any] = {}
    extra_context: dict[str, Any] = {}

    def get_next_lp_number(self, inventory):
        """Getting next ordinal number for Tree object"""
        trees = Tree.objects.filter(inventory=inventory)
        if not trees:
            return 1
        nr = trees.aggregate(Max("lp"))
        return nr.get("lp__max", 0) + 1

    def get(self, request, *args, **kwargs):
        inventory = get_object_or_404(Inventory, pk=kwargs["inventory_pk"])
        self.initial["inventory"] = inventory

        # initial ordinal number for new Tree in the form
        self.initial["lp"] = self.get_next_lp_number(inventory)
        return super().get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        try:
            return reverse_lazy(
                "inventory-details", args=[self.kwargs.get("inventory_pk")]
            )
        except Exception:
            return super().get_success_url()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["circuit_form"] = CircuitForm()
        return context

    def form_valid(self, form: TreeForm) -> HttpResponse:
        self.object = form.save()
        circuits = self.request.POST.getlist("circuit")
        for c in circuits:
            if c and c != "":
                Circuit.objects.create(tree=self.object, value=c)
        return HttpResponseRedirect(self.get_success_url())


class GaleryTreeView(LoginRequiredMixin, FormView):
    template_name = "TIS_app/tree_galery.html"
    form_class = PhotoTreeForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tree"] = get_object_or_404(
            Tree, lp=self.kwargs["lp"], inventory=self.kwargs["inventory_pk"]
        )
        return context

    def get_initial(self) -> Dict[str, Any]:
        data = super().get_initial()
        tree = get_object_or_404(
            Tree, lp=self.kwargs["lp"], inventory=self.kwargs["inventory_pk"]
        )
        data["tree"] = tree.pk
        return data

    def get_success_url(self) -> str:
        return reverse_lazy("tree-galery", kwargs=self.kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tree = get_object_or_404(Tree, pk=request.POST.get("tree"))
        images = request.FILES.getlist("image")
        if form.is_valid():
            for image in images:
                Photo.objects.create(tree=tree, image=image)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteInventoryView(DeleteView):
    model = Inventory
    success_url = reverse_lazy("all-inventory")
