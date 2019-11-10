from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/about', views.about, name='about')
]
