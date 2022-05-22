from django import forms
from django.contrib.auth import get_user_model

from TIS_app.models import Inventory, Photo, Tree, TreeComment
from TIS_app.validators import validate_password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        validators=[
            validate_password,
        ],
    )
    confirmation_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirmation_password",
        )
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if get_user_model().objects.filter(username=username):
            self.add_error("username", "Username is already taken !")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email):
            self.add_error(
                "email",
                "User with the given email already exists !",
            )
        return email

    def clean_confirmation_password(self):
        confirmation_password = self.cleaned_data.get("confirmation_password")
        password = self.cleaned_data.get("password")
        if password:
            if confirmation_password != password:
                self.add_error(
                    "confirmation_password",
                    "Passwords do not match !",
                )
        return confirmation_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = (
            "name",
            "principal",
            "principal_address",
            "description",
        )


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = (
            "name",
            "principal",
            "principal_address",
            "status",
            "description",
        )


class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = (
            "lp",
            "species",
            "height",
            "crown_width",
            "roloff",
            "inventory",
        )
        widgets = {"inventory": forms.HiddenInput(), "lp": forms.NumberInput()}
        labels = {"lp": "Identification number"}


class CircuitForm(forms.Form):
    circuit = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=600,
    )


class PhotoTreeForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("tree", "image")
        widgets = {
            "tree": forms.HiddenInput(),
            "image": forms.FileInput(attrs={"multiple": True}),
        }


class CommentTreeForm(forms.ModelForm):
    class Meta:
        model = TreeComment
        fields = ("tree", "description")
        widgets = {
            "tree": forms.HiddenInput(),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }
        labels = {
            "description": "",
        }
