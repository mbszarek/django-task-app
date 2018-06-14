import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class TaskCategory(models.Model):
    category_name = models.CharField(max_length=256)

    def __str__(self):
        return self.category_name


class Task(models.Model):
    task_name = models.CharField(max_length=256)
    task_description = models.CharField(max_length=1024)
    task_deadline = models.DateField('Task\'s deadline')
    task_category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return self.task_name

    def is_close_to_deadline(self):
        now = timezone.now()
        return now <= self.task_deadline <= now + datetime.timedelta(days=7)

    def is_available(self):
        now = timezone.now()
        return now <= self.task_deadline


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    tasks = models.ManyToManyField(Task)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, name=instance.username)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.name


class Comment(models.Model):
    comment_text = models.TextField(max_length=1024, blank=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task')
    date = models.DateTimeField('Publishing datetime')

    def __str__(self):
        return self.comment_text
