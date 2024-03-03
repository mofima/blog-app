from django.urls import path

from . import views


app_name = "item"
urlpatterns = [
    path("", views.index, name="index"),
    path("browse/", views.BrowseView.as_view(), name="browse"),
    path("new/", views.NewArticle.as_view(), name="new"),
    path("<uuid:pk>/", views.ArticleDetail.as_view(), name="detail"),
    path("<uuid:pk>/update/", views.ArticleUpdateView.as_view(), name="update"),
    path("<uuid:pk>/delete/", views.ArticleDeleteView.as_view(), name="delete"),
    path(
        "<uuid:pk>/comment/", views.CommentCreateView.as_view(), name="comment_create"
    ),
]
