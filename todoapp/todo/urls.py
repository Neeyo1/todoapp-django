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
    #todo
    path("todo/<int:todo_id>/", views.todo_detail, name="todo_detail"),
    path("todo/create/", views.todo_create, name="todo_create"),
    path("todo/edit/<int:todo_id>", views.todo_edit, name="todo_edit"),
    path("todo/delete/<int:todo_id>", views.todo_delete, name="todo_delete"),
    path("todo/complete/<int:todo_id>", views.todo_complete, name="todo_complete"),

]