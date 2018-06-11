from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Task, TaskCategory, Profile, Comment
from .forms import TaskForm, CategoryForm, LoginForm, RegisterForm, AddUserToTaskForm, CommentForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    headings = TaskCategory.objects.all()
    data = {cat: Task.objects.filter(task_category=cat.pk) for cat in headings}
    columns = [data[heading] for heading in headings]
    columns = list(map(lambda x: list(x), columns))
    if columns:
        max_len = len(max(columns, key=len))
        for col in columns:
            col += [None, ] * (max_len - len(col))
        rows = [[col[i] for col in columns] for i in range(max_len)]
    else:
        rows = None
    return render(request, 'tasks/index.html', context={
        'headings': headings,
        'rows': rows,
    })


@login_required(login_url='/login/')
def my_tasks(request, id):
    headings = TaskCategory.objects.all()
    data = {cat: Task.objects.filter(task_category=cat.pk) for cat in headings}
    user = get_object_or_404(Profile, pk=id)
    for key in data:
        data[key] = filter(lambda x: x in user.tasks.all(), data[key])
    columns = [data[heading] for heading in headings]
    columns = list(map(lambda x: list(x), columns))
    if columns:
        max_len = len(max(columns, key=len))
        for col in columns:
            col += [None, ] * (max_len - len(col))
        rows = [[col[i] for col in columns] for i in range(max_len)]
    else:
        rows = None
    return render(request, 'tasks/index.html', context={
        'headings': headings,
        'rows': rows,
    })


@login_required(login_url='/login/')
def task_detail(request, id):
    task = get_object_or_404(Task, pk=id)
    user = get_object_or_404(Profile, pk=request.user.pk)
    comments = Comment.objects.filter(task=task)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(comment_text=form['comment_text'].value(), author=user, task=task, date=timezone.now())
            comment.save()
            return redirect('tasks:task_detail', id)
    else:
        form = CommentForm()
    return render(request, 'tasks/task_detail.html', context={
        'task': task,
        'comments': comments,
        'form': form,
    })


@login_required(login_url='/login/')
def add_task(request, id):
    category = get_object_or_404(TaskCategory, pk=id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = Task(task_name=form['task_name'].value(), task_category=category,
                            task_description=form['task_description'].value(),
                            task_deadline=form['task_deadline'].value())
            new_task.save()
            return HttpResponseRedirect('/')
    else:
        form = TaskForm()
    return render(request, 'tasks/general_form.html', context={'form': form, 'string': 'New task'})


@login_required(login_url='/login/')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = TaskCategory(category_name=form['category_name'].value())
            new_category.save()
            return HttpResponseRedirect('/')
    else:
        form = CategoryForm()
    return render(request, 'tasks/general_form.html', context={'form': form, 'string': 'New category'})


@login_required(login_url='/login/')
def category_detail(request, id):
    category = get_object_or_404(TaskCategory, pk=id)
    return render(request, 'tasks/category_detail.html', context={'category': category})


@login_required(login_url='/login/')
def task_edit(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, initial={'task_name': task.task_name, 'task_description': task.task_description,
                                               'task_deadline': task.task_deadline})
        if form.is_valid():
            task.task_name = form['task_name'].value()
            task.task_description = form['task_description'].value()
            task.task_deadline = form['task_deadline'].value()
            task.save()
            return redirect('tasks:task_detail', id=task.pk)
    else:
        form = TaskForm(initial={'task_name': task.task_name, 'task_description': task.task_description,
                                 'task_deadline': task.task_deadline})
    return render(request, 'tasks/general_form.html', context={'form': form, 'string': 'Edit task'})


@login_required(login_url='/login/')
def category_edit(request, id):
    category = get_object_or_404(TaskCategory, pk=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, initial={'category_name': category.category_name})
        if form.is_valid():
            category.category_name = form['category_name'].value()
            category.save()
            return redirect('tasks:category_detail', id=category.pk)
    else:
        form = CategoryForm(initial={'category_name': category.category_name})
    return render(request, 'tasks/general_form.html', context={'form': form, 'string': 'Edit category'})


@login_required(login_url='/login/')
def category_delete(request, id):
    category = get_object_or_404(TaskCategory, pk=id)
    category.delete()
    return redirect('tasks:index')


@login_required(login_url='/login/')
def task_delete(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    return redirect('tasks:index')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['login'].value(), password=form['password'].value())
            if user is None:
                form = LoginForm()
                return render(request, 'tasks/login.html', context={'form': form, 'error_message': 'Login or password '
                                                                                                   'are incorrect'})
            else:
                login(request, user)
                return redirect('tasks:index')
    else:
        form = LoginForm()
    return render(request, 'tasks/login.html', context={'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form['username'].value()).count():
                form = RegisterForm()
                return render(request, 'tasks/register.html', context={'form': form,
                                                                       'error_message': 'Username exists in database.'
                                                                       })
            elif User.objects.filter(email=form['email'].value()).count():
                form = RegisterForm()
                return render(request, 'tasks/register.html', context={'form': form,
                                                                       'error_message': 'Email exists in database.'
                                                                       })
            user = User(username=form['username'].value(), email=form['email'])
            user.set_password(form['password'].value())
            user.save()
            return redirect('tasks:login')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', context={'form': form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('tasks:index')


@login_required(login_url='/login/')
def delete_user_from_task(request, task_id, user_id):
    task = get_object_or_404(Task, pk=task_id)
    user = get_object_or_404(Profile, pk=user_id)
    print(user.id)
    task.profile_set.remove(user)
    task.save()
    return redirect('tasks:task_detail', task_id)


@login_required(login_url='/login/')
def add_user_to_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        form = AddUserToTaskForm(request.POST)
        if form.is_valid():
            user_id = form['user'].value()
            user = get_object_or_404(Profile, pk=user_id)
            task.profile_set.add(user)
            task.save()
            return redirect('tasks:task_detail', id)
    else:
        form = AddUserToTaskForm()
    return render(request, 'tasks/general_form.html', context={
        'form': form,
        'string': 'Add user to task'
    })
