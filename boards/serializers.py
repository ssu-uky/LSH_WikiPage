from rest_framework import serializers

from .models import Board


class BoardPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = (
            "title",
            "content",
        )


class BoardListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Board
        fields = ("title", "created_at")


class BoardDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Board
        fields = (
            "title",
            "content",
            "related_board",
            "created_at",
            "updated_at",
        )

    read_only_fields = ("id", "related_board", "created_at", "updated_at")
