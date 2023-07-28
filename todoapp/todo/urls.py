from django.urls import path

from . import views

urlpatterns = [
    #main page
    path("", views.index, name="index")
]