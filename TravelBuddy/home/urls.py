from django.urls import path
from . import views

urlpatterns = [
    # MAKE "index" PAGE AS THE HOME PAGE OF THIS WEBSITE
    path('', views.index, name='index'),
]
