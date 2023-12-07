import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.conf import settings

from users.models import User
from .models import Board

client = APIClient()


@pytest.fixture()
def create_board():
    """
    게시글 생성
    """
    return Board.objects.create(
        title="test title",
        content="test content",
    )


@pytest.fixture()
def common_user(django_user_model):
    return django_user_model.objects.create_user(
        username="common_user",
        password="common123",
    )


@pytest.mark.django_db
def test_post_board(create_board):
    """
    게시글 생성 테스트
    """
    url = reverse("board-post")
    data = {
        "title": "new test title",
        "content": "new test content",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Board.objects.count() == 2
    assert response.data["message"] == "게시글 작성 완료"


@pytest.mark.django_db
def test_fail_post_board(create_board):
    """
    게시글 생성 실패 테스트
    """
    url = reverse("board-post")
    data = {
        "title": "new test title",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Board.objects.count() == 1
    assert response.data["content"][0] == "이 필드는 필수 항목입니다."


@pytest.mark.django_db
def test_get_board_list(create_board):
    """
    게시글 목록 조회 테스트
    """
    url = reverse("board-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    results = response.data["results"]
    assert len(results) == 1

    assert results[0]["title"] == "test title"
    assert "created_at" in results[0]


@pytest.mark.django_db
def test_get_board_pagination(create_board):
    """
    게시글 목록 조회 테스트 (페이지네이션)
    """
    url = reverse("board-list")
    response = client.get(url, {"page": 3})

    for _ in range(30):
        Board.objects.create(title="Test Title", content="Test Content")

    # 첫 번째 페이지 요청
    url = reverse("board-list") + "?page=1"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) <= settings.PAGE_SIZE

    # 두 번째 페이지 요청
    url = reverse("board-list") + "?page=2"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) <= settings.PAGE_SIZE

    # 유효하지 않은 페이지 번호 요청
    url = reverse("board-list") + "?page=1000"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 0


@pytest.fixture()
def create_board_and_related():
    """
    메인 게시글 및 연관된 게시글 생성
    """
    main_board = Board.objects.create(
        title="Python 강의 추천",
        content=" Python 그리고 Django 와 Flask , FastAPI 로 부탁드립니다.",
    )

    related_boards_contents = [
        "CSS 강의, CSS 디자인 패턴 배우기.",
        "HTML 강의, HTML5와 CSS3의 새로운 기능.",
        "Python 강의, Java와 Python 비교.",
        "JavaScript 강의, Java 스크립트로 인터랙티브 웹 만들기.",
        "Django 강의, Python 기반의 Django 프레임워크 소개.",
    ]

    for content in related_boards_contents:
        related_board = Board.objects.create(
            title=f"{content.split()[0]}", content=content
        )
        main_board.related_board.add(related_board)

    return main_board


# GET
@pytest.mark.django_db
def test_get_board_detail(create_board_and_related):
    boards = create_board_and_related
    url = reverse("board-detail", kwargs={"id": boards.id})

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == boards.id
    assert response.data["title"] == boards.title
    assert "related_boards_count" in response.data
    assert len(response.data["related_board"]) == len(boards.related_board.all())

    for related_board_data in response.data["related_board"]:
        assert "title" in related_board_data
        assert "total_count" in related_board_data
        assert "word_counts" in related_board_data


# PUT
@pytest.mark.django_db
def test_put_board_detail_by_admin(create_board, admin_user):
    """
    게시글 수정 테스트 (관리자 권한)
    """
    client.force_authenticate(user=admin_user)  # 관리자 권한 부여
    url = reverse("board-detail", kwargs={"id": create_board.id})
    data = {"title": "Updated Title", "content": "Updated Content"}
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "게시글 수정 완료"


@pytest.mark.django_db
def test_put_board_detail_by_common_user(create_board, common_user):
    """
    게시글 수정 실패 테스트 (유저는 권한 없음)
    """
    client.force_authenticate(user=common_user)
    url = reverse("board-detail", kwargs={"id": create_board.id})
    data = {"title": "change title", "content": "change Content"}
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["message"] == "해당 게시글을 수정할 권한이 없습니다."


# DELETE
@pytest.mark.django_db
def test_delete_board_detail_by_admin(create_board, admin_user):
    """
    게시글 삭제 테스트 (관리자 권한)
    """
    client.force_authenticate(user=admin_user)
    url = reverse("board-detail", kwargs={"id": create_board.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "게시글 삭제 완료"
    assert Board.objects.filter(id=create_board.id).count() == 0


@pytest.mark.django_db
def test_delete_board_detail_common_user(create_board, common_user):
    """
    게시글 삭제 실패 테스트 (유저는 권한 없음)
    """
    client.force_authenticate(user=common_user)
    url = reverse("board-detail", kwargs={"id": create_board.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["message"] == "해당 게시글을 삭제할 권한이 없습니다."
    assert Board.objects.filter(id=create_board.id).count() == 1
