from django.urls import path

from . import views

urlpatterns = [
    #main page
    path("", views.index, name="index"),
    #login
    path("login/", views.login_to_page, name="login_to_page"),
    #logout
    path("logout/", views.logout_from_page, name="logout_from_page"),
    #register
    path("register/", views.register_to_page, name="register_to_page"),

]