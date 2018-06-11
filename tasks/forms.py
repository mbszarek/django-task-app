from django import forms
from .models import Profile


class TaskForm(forms.Form):
    task_name = forms.CharField(max_length=256)
    task_description = forms.CharField(max_length=1024)
    task_deadline = forms.DateField(widget=forms.SelectDateWidget())


class CategoryForm(forms.Form):
    category_name = forms.CharField(max_length=256)


class LoginForm(forms.Form):
    login = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32)
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class AddUserToTaskForm(forms.Form):
    user = forms.ChoiceField(choices=[(user.id, user.name) for user in Profile.objects.all()])


class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=1024, widget=forms.Textarea(), label='')
