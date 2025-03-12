from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:categ>", views.category, name="category"),
    path("newpost", views.newpost, name="newpost"),
    path("togglelike/<int:post_id>", views.togglelike, name="togglelike"),
    path("addcomment/<int:post_id>", views.addcomment, name="addcomment"),
    path("addtag/<int:post_id>", views.addtag, name="addtag"),
    path("togglecommentlike/<int:comment_id>", views.togglecommentlike, name="togglecommentlike"),
    path("searchtag", views.searchtag, name="searchtag"),
    path("dasearchpage", views.dasearchpage, name="dasearchpage"),
    path("subjectsearchtag", views.subjectsearchtag, name="subjectsearchtag"),
    path("yourposts", views.yourposts, name="yourposts"),
    path("yourpostssearch", views.yourpostssearch, name="yourpostssearch")
    ]