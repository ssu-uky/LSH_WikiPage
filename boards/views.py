from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from collections import Counter
from django.conf import settings

from .serializers import BoardPostSerializer, BoardListSerializer, BoardDetailSerializer
from .models import Board


# http://127.0.0.1:8000/api/v1/boards/post/
class BoardPostView(APIView):
    """
    POST : 게시글 작성
    """

    def get(self, request):
        return Response({"message": "title, content 를 입력해주세요."})

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"message": "게시글은 관리자만 작성할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BoardPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "게시글 작성 완료",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# http://127.0.0.1:8000/api/v1/boards/list/?page="숫자"
class BoardListView(APIView):
    """
    GET : 게시글 목록 조회
    """

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = page_size * (page - 1)
        end = start + page_size

        boards = Board.objects.all().order_by("-created_at")
        serializer = BoardListSerializer(boards[start:end], many=True)
        return Response(
            {"count": len(boards), "results": serializer.data},
            status=status.HTTP_200_OK,
        )


# http://127.0.0.1:8000/api/v1/boards/<int:board_id>/
class BoardDetailView(APIView):
    """
    GET : 게시글 상세 조회 (연관 게시글 포함)
    PUT : 게시글 수정 (관리자만 가능)
    DELETE : 게시글 삭제 (관리자만 가능)
    """

    def get_object(self, request, id):
        try:
            return Board.objects.get(id=id)
        except Board.DoesNotExist:
            return None

    # 전체 게시글에서 단어들의 출현 빈도를 계산
    def get_word_frequencies(self):
        all_boards = Board.objects.all()
        all_words = [word for board in all_boards for word in board.content.split()]
        word_counter = Counter(all_words)
        total_count = len(all_words)
        return {word: count / total_count for word, count in word_counter.items()}

    # 연관 게시물 찾기
    def get_related_boards(self, board_id, content):
        word_frequencies = self.get_word_frequencies()
        words = content.split()

        excluded_words = {word for word, freq in word_frequencies.items() if freq > 0.6}

        candidate_boards = Board.objects.exclude(id=board_id)

        related_boards_info = {}

        for board in candidate_boards:
            board_word_counts = Counter(
                word
                for word in board.content.split()
                if word in words and word not in excluded_words
            )
            included_words = {
                word
                for word, count in board_word_counts.items()
                if word_frequencies.get(word, 0) <= 0.4 and count >= 2
            }

            if included_words:
                total_count = sum(board_word_counts[word] for word in included_words)
                related_boards_info[board] = {
                    "total_count": total_count,
                    "word_counts": {
                        word: board_word_counts[word] for word in included_words
                    },
                }

        sorted_related_boards = sorted(
            related_boards_info.items(),
            key=lambda item: item[1]["total_count"],
            reverse=True,
        )
        return sorted_related_boards

    def get(self, request, id):
        board = self.get_object(request, id)
        if board is None:
            return Response(
                {"message": "해당 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        related_boards_data = self.get_related_boards(id, board.content)

        related_boards = [board[0] for board in related_boards_data]
        board.related_board.set(related_boards)
        board.save()

        related_boards_count = len(related_boards)

        data = {
            "related_boards_data": dict(related_boards_data),
            "related_boards_count": related_boards_count,
        }

        serializer = BoardDetailSerializer(board, context=data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        if not request.user.is_staff:
            return Response(
                {"message": "해당 게시글을 수정할 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )
        board = self.get_object(request, id)
        serializer = BoardPostSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글 수정 완료"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if not request.user.is_staff:
            return Response(
                {"message": "해당 게시글을 삭제할 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )
        board = self.get_object(request, id)
        board.delete()
        return Response({"message": "게시글 삭제 완료"}, status=status.HTTP_200_OK)
