# from allauth.socialaccount.models import SocialApp

from django.contrib import admin

from TIS_app.models import (
    Circuit,
    Inventory,
    ManagementTree,
    Photo,
    Species,
    Tree,
    TreeComment,
    ValorizationTree,
)


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    pass


@admin.register(TreeComment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    pass


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    pass


@admin.register(ValorizationTree)
class ValorizationTreeAdmin(admin.ModelAdmin):
    pass


@admin.register(ManagementTree)
class ManagementTreeAdmin(admin.ModelAdmin):
    pass
