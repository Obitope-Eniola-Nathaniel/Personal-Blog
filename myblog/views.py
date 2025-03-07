from django.shortcuts import render
import json
import os
from datetime import datetime
from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import RegisterForm



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, your account is created')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

# Create your views here.

# JSON file to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(title, content):
    """Add a new task."""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "content": content,
        "createdAt": str(datetime.now()),
    }
    tasks.append(new_task)
    save_tasks(tasks)

def update_task(task_id, title, content):
    """Update task status."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            task["content"] = content
            save_tasks(tasks)
            print(f"Task {task_id} updated to {title}")
            return
    print("Task not found.")

def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted.")

def index(request):
    tasks = load_tasks()
    return render(request, "index.html", {"tasks": tasks})

def article_page(request, id):
    tasks = load_tasks()
    task = tasks[int(id) - 1]
    return render(request, "article_page.html", {"task": task})


@login_required
def admin(request):
    tasks = load_tasks()
    return render(request, "admin.html", {"tasks": tasks})



def delete(request, id):
    task = int(id)
    delete_task(task)
    tasks = load_tasks()
    return render(request, "admin.html", {"tasks": tasks})


def edit(request, id):
    task = int(id) - 1
    tasks = load_tasks()    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        update_task(int(id), title, content)
        tasks = load_tasks() 
        return render(request, "admin.html", {"tasks": tasks})
    else:
        return render(request, "edit.html", {"task": tasks[task]})

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        add_task(title, content)
        return redirect("home")
    return render(request, "create.html")