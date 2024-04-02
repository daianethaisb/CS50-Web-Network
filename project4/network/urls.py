
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("profile/<int:userId>", views.profile, name="profile"),
    path("follow_unfolow/<int:userId>", views.follow_unfolow, name="follow_unfolow"),
    path("following", views.following, name="following"),
    path("editPost/<int:postId>", views.editPost, name="editPost"),
    path("likePost/<int:postId>", views.likePost, name="likePost"),
    path("unlikePost/<int:postId>", views.unlikePost, name="unlikePost")
]
