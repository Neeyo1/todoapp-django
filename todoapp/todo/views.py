from django.shortcuts import render
from .models import Todo
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    context = {}
    todo_items = Todo.objects.all()
    context['todo_items'] = todo_items
    return render(request, "todo/index.html", context)