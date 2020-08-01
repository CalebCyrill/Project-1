from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:pagename>", views.page, name="page"),
    path("search/", views.search, name="searchresults"),
    path("create", views.create, name="create"),
    path("newpage", views.newPage, name="newpage"),
    path("exists", views.exist, name="exists"),
    path("editpage/<str:name>", views.editPage, name="editpage"),
    path("edit", views.edit, name="edit"),
    path("random", views.randomPage, name="random")
]
