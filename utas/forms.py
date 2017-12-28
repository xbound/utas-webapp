from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import EmailTask


class EmailTaskForm(forms.ModelForm):
    class Meta:
        model = EmailTask
        exclude = ['task_id','user_id','submition_datetime']
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of task...'}),
            'task_description': forms.Textarea(attrs={'class': 'form-control', "placeholder": "Description of task..."}),
            'to_email': forms.EmailInput(attrs={'type': 'email', 'class': 'form-control', "placeholder": "email@example.com"}),
            'subject': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Subject of email..."}),
            'message': forms.Textarea(attrs={'class': 'form-control', "placeholder": "Your message..."}),
            'execution_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', "placeholder": "day/month/Year H:m"}),
            'execution_time': forms.TimeInput(attrs={'class': 'form-control', "placeholder": "h:m"})
        }

    def clean_execution_date(self):
        date = self.cleaned_data['execution_date']
        if date < datetime.now().date():
            raise ValidationError(_("Invalid scheduled date: %(date)s"),params={'date': date.strftime("%d/%m/%Y")})
        return date

    def clean_execution_time(self):
        time = self.cleaned_data['execution_time']
        date = self.cleaned_data.get('execution_date')
        today_now = datetime.now()
        if time <= today_now.time():
            if date == today_now.date():
                raise ValidationError(_("Invalid scheduled time: %(time)s"),params={'time': time.strftime("%H:%M")})
        return time
