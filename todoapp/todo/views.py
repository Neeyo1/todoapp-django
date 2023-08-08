from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Todo
from .forms import TodoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    context = {}
    if request.user.is_authenticated:
        #todo_items = Todo.objects.filter(author=request.user)
        q_todo = request.GET.get('type') or ''
        if q_todo in ('All', ''):
            todo_items = Todo.objects.filter(author=request.user)
        elif q_todo == 'Open':
            todo_items = Todo.objects.filter(author=request.user, completed=False)
        elif q_todo == 'Closed':   
            todo_items = Todo.objects.filter(author=request.user, completed=True)
        try:
            context['todo_items'] = todo_items
            context['q_todo'] = q_todo
        except:
            pass
    return render(request, "todo/index.html", context)

def todo_detail(request, todo_id):
    context = {}
    todo = get_object_or_404(Todo, pk=todo_id)
    context["todo"] = todo
    return render(request, "todo/todo_detail.html", context)

def todo_create(request):
    context = {}
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect("/")
    else:
        form = TodoForm()
    context["form"] = form
    return render(request, "todo/create_edit_form.html", {"form": form})

def todo_edit(request, todo_id):
    context = {}
    todo = get_object_or_404(Todo, pk=todo_id)

    if request.user != todo.author:
        return HttpResponse("You are not author of this todo")

    form = TodoForm(instance=todo)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(f"/todo/{instance.id}/")
    context["form"] = form
    return render(request, "todo/create_edit_form.html", context)

def todo_delete(request, todo_id):
    context = {}
    todo = get_object_or_404(Todo, pk=todo_id)

    if request.user != todo.author:
        return HttpResponse("You are not author of this todo")

    if request.method == "POST":
        todo.delete()
        return HttpResponseRedirect("/")
    context["object_to_delete"] = todo
    return render(request, "todo/delete_form.html", context)

def todo_complete(request, todo_id):
    context = {}
    todo = get_object_or_404(Todo, pk=todo_id)

    if request.user != todo.author:
        return HttpResponse("You are not author of this note")
    
    if request.method == "POST":
        todo.completed = not todo.completed
        todo.save()
        return HttpResponseRedirect(f"/todo/{todo.id}")

    context["object_to_complete"] = todo
    return render(request, "todo/complete_form.html", context)

def login_to_page(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Success")
            next_url = request.GET.get('next') or "/"
            return HttpResponseRedirect(next_url)
        else:
            error_message = "Incorrect login or password"
            context["error_message"] = error_message
            return render(request, "todo/login_form.html", context)
    return render(request, "todo/login_form.html", context)

def logout_from_page(request):
    logout(request)
    return HttpResponseRedirect("/")

def register_to_page(request):
    context = {}
    form = UserCreationForm()
    context["form"] = form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            error_message = "Error during registration"
            context["error_message"] = error_message
            context["form"] = form
            return render(request, "todo/register_form.html", context)
    return render(request, "todo/register_form.html", context)