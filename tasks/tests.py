import datetime
from django.test import TestCase
from django.utils import timezone

# Create your tests here.

from .models import Task


class TaskModelTests(TestCase):

    def past_task_available(self):
        time = timezone.now() - datetime.timedelta(days=2)
        past_task = Task(task_deadline=time)
        self.assertIs(past_task.is_available(), False)

    def past_task_close_to_deadline(self):
        time = timezone.now() - datetime.timedelta(days=2)
        past_task = Task(task_deadline=time)
        self.assertIs(past_task.is_close_to_deadline(), False)

    def future_task_available(self):
        time = timezone.now() + datetime.timedelta(days=1)
        future_task = Task(task_deadline=time)
        self.assertIs(future_task.is_available(), True)

    def future_task_close_to_deadline(self):
        time = timezone.now() + datetime.timedelta(days=1)
        future_task = Task(task_deadline=time)
        self.assertIs(future_task.is_close_to_deadline(), True)

    def future_task_not_close(self):
        time = timezone.now() + datetime.timedelta(days=31)
        future_task = Task(task_deadline=time)
        self.assertIs(future_task.is_available(), True)
        self.assertIs(future_task.is_close_to_deadline(), False)
