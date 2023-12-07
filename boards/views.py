from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import BoardPostSerializer, BoardListSerializer, BoardDetailSerializer
from .models import Board


class BoardPostView(APIView):
    """
    POST : 게시글 작성
    """

    def get(self, request):
        return Response({"message": "title, content 를 입력해주세요."})

    def post(self, request):
        serializer = BoardPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글 작성 완료"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardListView(APIView):
    """
    GET : 게시글 목록 조회
    """

    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardListSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardDetailView(APIView):
    """
    GET : 게시글 상세 조회 (연관 게시글 포함)
    PUT : 게시글 수정
    DELETE : 게시글 삭제
    """

    def get_object(self, request, id):
        try:
            return Board.objects.get(id=id)
        except Board.DoesNotExist:
            return Response(
                {"message": "해당 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, id):
        board = self.get_object(request, id)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        board = self.get_object(request, id)
        serializer = BoardPostSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글 수정 완료"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        board = self.get_object(request, id)
        board.delete()
        return Response({"message": "게시글 삭제 완료"}, status=status.HTTP_200_OK)
