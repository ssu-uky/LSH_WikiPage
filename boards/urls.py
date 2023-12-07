from django.urls import path
from . import views


urlpatterns = [
    path("post/", views.BoardPostView.as_view(), name="board_post"),
    path("list/", views.BoardListView.as_view(), name="board_list"),
    path("<int:id>/", views.BoardDetailView.as_view(), name="board_detail"),
]
