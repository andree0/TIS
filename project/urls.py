"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# from TIS_app import routers as r
from TIS_app import views as v

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", v.IndexView.as_view(), name="index"),
    path("register/", v.RegisterView.as_view(), name="register"),
    path(
        "inventory/create/",
        v.CreateNewInventoryView.as_view(),
        name="create-inventory",
    ),
    path("inventory/all/", v.AllInventoryView.as_view(), name="all-inventory"),
    path(
        "inventory/<int:pk>/details/",
        v.UpdateInventoryView.as_view(),
        name="inventory-details",
    ),
    path(
        "inventory/<int:inventory_pk>/tree/add/",
        v.AddTreeToInventoryView.as_view(),
        name="tree-add",
    ),
    path(
        "inventory/<int:inventory_pk>/tree/<int:lp>/",
        v.GaleryTreeView.as_view(),
        name="tree-galery",
    ),
    path(
        "inventory/<int:pk>/delete/",
        v.DeleteInventoryView.as_view(),
        name="delete-inventory",
    ),
    # API urls
    path(
        "api/inventory/<int:pk>/details/",
        v.DetailInventoryAPIView.as_view(),
        name="api-inventory-details",
    ),
    path(
        "api/inventory/add-photo-tree/",
        v.AddPhotoTreeAPIView.as_view(),
        name="api-add-photo-tree",
    ),
    path(
        "api/inventory/add-comment-tree/",
        v.AddCommentTreeAPIView.as_view(),
        name="api-add-comment-tree",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
