from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("searchresult", views.searchResult, name="searchresult"),
    path("randompage", views.randomPage, name="randomPage"),
    path("newpage", views.newPage, name="newPage"),
    path("editpage", views.editPage, name="editPage"),
    path("<str:title>", views.entryPage, name="entryPage")
]
