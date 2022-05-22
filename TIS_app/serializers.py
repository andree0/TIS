from django.contrib.auth import get_user_model
from rest_framework import serializers

from TIS_app.models import Circuit, Inventory, Photo, Tree, TreeComment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="TIS_app:user-detail")

    class Meta:
        model = get_user_model()
        fields = ["url", "username", "email", "is_staff"]


class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ("value",)


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = (
            "name",
            "description",
            "author",
            "principal",
            "principal_address",
            "status",
            "created_date",
        )
        read_only_fields = ("created_date",)


class PhotoTreeSerializer(serializers.ModelSerializer):
    tree = serializers.PrimaryKeyRelatedField(queryset=Tree.objects.all())
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, use_url=True
    )

    class Meta:
        model = Photo
        fields = (
            "tree",
            "image",
        )


class CommentTreeSerializer(serializers.ModelSerializer):
    tree = serializers.PrimaryKeyRelatedField(queryset=Tree.objects.all())

    class Meta:
        model = TreeComment
        fields = (
            "tree",
            "description",
            "created",
        )
        read_only_fields = ("created",)
