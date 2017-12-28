from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.db import models
from celery.result import AsyncResult
from utas.tasks import send_email


class UtasTask(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    task_id = models.CharField(max_length=255,blank=False)
    task_name = models.CharField(max_length=50, blank=False, verbose_name='Task name:')
    task_description = models.CharField(max_length=300, blank=True, verbose_name='Task description:')
    submition_datetime = models.DateTimeField(auto_now_add=True)
    execution_date = models.DateField(null=False, verbose_name='Scheduled date:')
    execution_time = models.TimeField(null=False, verbose_name='Scheduled time:')

    def eta(self):
        eta = datetime.combine(self.execution_date,self.execution_time)
        return timezone.make_aware(eta,timezone.get_current_timezone())

    def status(self):
        return AsyncResult(self.task_id).state

    def revoke(self):
        AsyncResult(self.task_id).revoke(terminate=True,signal='SIGKILL')
        return self


class EmailTask(UtasTask):
    to_email = models.EmailField(max_length=50, null=False, verbose_name='Send to:')
    subject = models.CharField(max_length=50, blank=False, verbose_name='Email subject:')
    message = models.CharField(max_length=700, blank=True, verbose_name='Email massage:')

    def submit(self):
        self.task_id = send_email.apply_async((self.subject,
        self.message,settings.EMAIL_HOST_USER,[self.to_email]),eta=self.eta()).id
        return self

    def get_absolute_url(self):
        return reverse('update_email_task',args=[str(self.id)])
