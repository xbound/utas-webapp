from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True)
def send_email(self,subject,message,from_email,to_list: list):
    try:
        send_mail(subject,message,from_email,to_list,fail_silently=False)
    except BadHeaderError:
        return "Invalid header found"
    return "Message sent..."
