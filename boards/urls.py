from django.urls import path
from . import views


urlpatterns = [
    path("post/", views.BoardPostView.as_view(), name="board-post"),
    path("list/", views.BoardListView.as_view(), name="board-list"),
    path("<int:id>/", views.BoardDetailView.as_view(), name="board-detail"),
]
