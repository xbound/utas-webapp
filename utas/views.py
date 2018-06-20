from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.http import HttpResponseServerError,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404

from utas.forms import EmailTaskForm
from utas.models import UtasTask, EmailTask


@require_http_methods("GET")
@login_required
def home_page(request):
    return render(request,'utas/home.html', context={'header': 'Home'})

@require_http_methods("GET")
@login_required
def get_tasks(request):
    tasks = EmailTask.objects.filter(user_id=request.user)
    context = {'tasks':tasks}
    tasks_table = render_to_string('utas/includes/tasks_list.html',context,request=request)
    return JsonResponse({'tasks_table':tasks_table})

@require_http_methods("POST")
@login_required
def remove_task(request):
    task = get_object_or_404(UtasTask,pk=request.POST.get('pk'),user_id=request.user)
    context = dict()
    try:
        task.revoke()
        task.delete()
    except Exception as e:
        context['info'] = "Failed to remove task!"
        context['success'] = False
    else:
        context['info'] = "Task removed successfully!"
        context['success'] = True
    return JsonResponse(context)

class CreateEmailTask(LoginRequiredMixin,TemplateView):
    template_name = 'utas/email_task_view.html'
    header = 'Create email task'

    def get(self, request):
        context = {'form':EmailTaskForm(),'header':self.header}
        return render(request, self.template_name, context=context)

    def post(self, request):
        task_form = EmailTaskForm(request.POST)
        if not task_form.is_valid():
            context = {'form':task_form,'header':self.header}
            return render(request, self.template_name, context=context)
        task = task_form.save(commit=False)
        task.user_id = request.user
        task.submit().save()
        context = {'form':EmailTaskForm(),'header':self.header,'success':True,'info':'Task created successfully!'}
        return render(request, self.template_name, context=context)

class EditEmailTask(LoginRequiredMixin,TemplateView):
    template_name = 'utas/email_task_view.html'
    header = 'Edit email task'

    def get(self, request,pk):
        task = get_object_or_404(EmailTask,pk=pk,user_id=request.user)
        context = {'form':EmailTaskForm(instance=task),'header':self.header,'pk':task.id}
        return render(request, self.template_name, context=context)

    def post(self, request,pk):
        task = get_object_or_404(EmailTask,pk=pk,user_id=request.user)
        task_form = EmailTaskForm(request.POST)
        if not task_form.is_valid():
            context = {'form':task_form,'header':self.header}
            return render(request, self.template_name, context=context)
        updated_task = task_form.save(commit=False)
        updated_task.user_id = request.user
        try:
            updated_task.submit().save()
            task.revoke().delete()
        except Exception as e:
            return HttpResponseServerError()
        else:
            return redirect('home')
