from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name = "entry"),
    path("wiki/edit/<str:name>", views.edit, name = "edit"     ),
    path("search", views.search, name = "search"   ),
    path("create_page", views.create_page, name = "create_page"),
    path("create_page_error", views.create_page_error, name = "create_page_error"),
    path("random_page", views.random_page, name = "random_page")
    
]
