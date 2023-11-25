from django.urls import path
from library_app.books import views

urlpatterns = [
    path('', views.index),
]