from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url
from .views import home_page, get_tasks, remove_task, CreateEmailTask, EditEmailTask

urlpatterns = [
    url(r'^home/$', home_page, name='home'),
    url(r'^tasks/$', get_tasks, name='tasks'),
    url(r'^login/$', LoginView.as_view(template_name='utas/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^create/email_task/$', CreateEmailTask.as_view(), name='create_email_task'),
    url(r'^update/email_task/(?P<pk>\d+)$', EditEmailTask.as_view(), name='update_email_task'),
    url(r'^remove/', remove_task, name='remove_email_task'),
]
