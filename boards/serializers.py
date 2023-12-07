from rest_framework import serializers

from .models import Board


class BoardPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "content",
        )


class BoardListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Board
        fields = ("id", "title", "created_at")


class BoardDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    related_board = serializers.SerializerMethodField()
    related_boards_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "content",
            "related_boards_count",
            "related_board",
            "created_at",
            "updated_at",
        )

    read_only_fields = ("id", "related_board", "created_at", "updated_at")

    def get_related_board(self, obj):
        # Serializer context에서 연관 게시글 데이터를 가져옵니다.
        related_boards_data = self.context.get("related_boards_data", {})
        related_boards_info = []
        for board, data in related_boards_data.items():
            board_info = BoardPostSerializer(board).data
            board_info.update(data)  # 연관된 단어와 출현 횟수 정보를 추가합니다.
            related_boards_info.append(board_info)
        return related_boards_info

    def get_related_boards_count(self, obj):
        # Serializer context에서 연관 게시글 데이터를 가져옵니다.
        return self.context.get("related_boards_count", 0)
