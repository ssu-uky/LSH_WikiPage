from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import SignupSerializer, LoginSerializer

# 127.0.0.1:8000/api/v1/users/signup/
class SignUpView(APIView):
    """
    POST : 회원가입
    """

    def get(self, request):
        return Response({"message": "username, name, password를 입력해주세요."})

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user_pk": user.pk,
                    "name": user.name,
                    "username": user.username,
                    "message": f"{user.username}님, 회원가입이 완료되었습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
