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


class LoginView(APIView):
    """
    POST : 로그인
    """

    def get(self, request):
        return Response({"message": "username, password를 입력해주세요."})

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"message": "username, password를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": f"{user.username}님, 로그인 되었습니다."})

        else:
            return Response(
                {"message": "아이디 또는 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """
    POST : 로그아웃
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
