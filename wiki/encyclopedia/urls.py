from django.urls import path

from . import views,util

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:query>', views.query , name = "query"),
    path("pages/random", views.random, name='random'),
    path("pages/create", views.create, name='create'),
    path("pages/pages/new", views.new, name='new'),
    path("pages/edit", views.edit, name='edit'),
    path("pages/submit_edit", views.sub_edit, name='submit_edit')
]
