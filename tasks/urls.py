from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('task/<int:id>/', views.task_detail, name='task_detail'),
    path('category/<int:id>/add_task', views.add_task, name='add_task'),
    path('task/<int:id>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:id>/delete/', views.task_delete, name='task_delete'),
    path('category/', views.add_category, name='add_category'),
    path('category/<int:id>', views.category_detail, name='category_detail'),
    path('category/<int:id>/edit', views.category_edit, name='category_edit'),
    path('category/<int:id>/delete', views.category_delete, name='category_delete'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('my_tasks/<int:id>', views.my_tasks, name='my_tasks'),
    path('task/<int:task_id>/user/delete/<int:user_id>', views.delete_user_from_task, name='delete_user_from_task'),
    path('task/<int:id>/user/add/', views.add_user_to_task, name='add_user_to_task'),
    path('tasks/available/', views.available_tasks, name='available_tasks'),
]
