#_*_coding:utf-8_*_
from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import status
import serializers 
import models
import json
import time,random
from rest_framework.response import Response
from rest_framework.decorators import api_view
import custom_forms
from django.forms.models import modelformset_factory
from django.template import  RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
# Create your views here.


def login_page(request):
    return render_to_response('login.html',context_instance = RequestContext(request))

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_empty = all([username,password])
        if not is_empty:
            return render_to_response('login.html',{'error':"���ݲ���Ϊ��.",'username':username if username else '','pwd':password if password else '' })

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            go_to = '/'
            next = request.GET.get('next',None)
            if next:
                go_to = next
                
            return HttpResponseRedirect(go_to)
        else:
            return render_to_response('login.html',{'error':"�û����������������.",'username':username,'pwd':password })
    else:
        return render_to_response('login.html',{'error':"",'username':'','pwd':'' })

        
def Logout(request,arg):
    auth.logout(request)
    return HttpResponseRedirect('/login')

class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset =  models.Host.objects.all()
    serializer_class = serializers.HostSerializer 
    
def monitor_data(request):
    print request.POST 
    
    return HttpResponse('service sends status report success!!')


def graph(request):
    return render_to_response('index.htm')


def graph_data(request):
    '''fake_data = [[1230771600000, -5.8, 0.1],
        [1230858000000, -4.1, 1.4],
        [1230944400000, -0.5, 4.1],
        [1231030800000, -8.9, -0.7],
        [1231117200000, -9.7, -3.7],
        [1231203600000, -3.4, 3.2]]
    '''
    fake_data = []
    start_num = 86400
    for i in range(86400):
        point = [(time.time() -start_num)*1000, random.randrange(100) ]
        fake_data.append(point)
        start_num -=1
        
    
    return HttpResponse(json.dumps(fake_data))


###############below for task allocations #######################


class  TaskCenterViewSet(viewsets.ModelViewSet):
    #print self.REQUEST
    queryset = models.TaskCenter.objects.all()
    serializer_class = serializers.TaskCenterSerializer
    

class HostProfileViewSet(viewsets.ModelViewSet):
    queryset =  models.Host.objects.all()
    serializer_class = serializers.HostProfileSerializer     


@api_view(['GET'])
def new_tasks(request,last_task_id):
        
    query_set = models.TaskCenter.objects.filter(id__gt=last_task_id)
    print '---->',query_set
    serializer_class = serializers.TaskCenterSerializer(query_set,many=True)
    #return Response(serializer_class.data,status=status.HTTP_300_MULTIPLE_CHOICES)
    return Response(serializer_class.data)

@api_view(['POST'])
def task_result(request):       
    
    
    print '-->',request.POST 
    host_profile = request.POST.get('host_profile')
    task_status = request.POST.get('status')
    task_result = request.POST.get('run_log')
    print '-----115----'
    task_profile = json.loads(request.POST.get('task'))
    
    print '-----117----',task_profile
    host_profile = json.loads(host_profile)
    print '---120:',type(task_profile),task_profile['id']
    task_obj = models.TaskCenter.objects.get(id=task_profile.get('id'))
    models.TaskLog.objects.create(task=task_obj,
                                  result=task_status,
                                  log = task_result,
                                  host_id = host_profile.get('id')
                                  )
    
    return HttpResponse('...result submitted...')





###########below for web pages ###############

@login_required
def task_center(request):
    form = custom_forms.TaskCenterForm()
    #task_list = models.TaskCenter.objects.all()
    task_list  = []
    
    for task in models.TaskCenter.objects.all():
        task_info = {'id':task.id,
                     'name':task.name,
                     'description':task.description,
                     'task_type':task.task_type,
                     'hosts':task.hosts,
                     'groups':task.groups,
                     'created_by':task.created_by,
                     'kick_off_at':task.kick_off_at,
                     'total_tasks':task.hosts.select_related().count(),
                     'failure':models.TaskLog.objects.filter(task_id=task.id,result='failed').count(),
                     'success':models.TaskLog.objects.filter(task_id=task.id,result='success').count(),
                     'is_template':task.is_template
                     }
    
        task_list.append(task_info)
        print task_info['failure']
        print task_info['success']
    return render_to_response('task_center.html',{'form':form,
                                            'task_list':task_list,
                                            'request':request})

def new_task(request):

    form = custom_forms.TaskCenterForm(request.POST,request.FILES)
    print request.POST
    
    if form.is_valid():
        print 'form is valid'
        #form.cleaned_data['created_by'] = models.UserProfile.objects.all()[0]
        print  form.cleaned_data
        form.save()
        return HttpResponseRedirect('/task_center/')
    else:
        print form.errors
        return render_to_response('task_center.html',{'form':form})

def task_detail(request,task_id):
    
    return render_to_response('task_detail.html',{'task_id':task_id})   


def task_logs(request,task_id):
    
    
    success_count = models.TaskLog.objects.filter(task_id=task_id,result='success').count()
    failure_count = models.TaskLog.objects.filter(task_id=task_id,result='failure').count()
    task_hosts = models.TaskCenter.objects.get(id=task_id).hosts.select_related()
    task_groups = models.TaskCenter.objects.get(id=task_id).groups.select_related()
    total_tasks = [] 
    total_tasks.extend(task_hosts) 
    
    for group in task_groups:
        total_tasks += models.Host.objects.filter(group__name = group.name)
    
    print total_tasks
    print set(total_tasks)
    log_list =[]
    for log in models.TaskLog.objects.filter(task_id=task_id):
        host = models.Host.objects.get(id=log.host_id)
        log_dic = {'result': log.result,
                   'log': log.log,
                   'host': host.hostname,
                   'ip': host.ip,
                   'date': log.date.strftime("%Y-%m-%d %H:%M:%S")}
        log_list.append(log_dic)
    
    task_detail = {'success_count': success_count,
                   'failure_count': failure_count,
                   'total_task': len(set(total_tasks)),
                   'log_list': log_list}
    
    return HttpResponse(json.dumps(task_detail))
def cmdb(request):
    
    return render_to_response('cmdb.html')   
def monitor(request):
    
    return render_to_response('monitor.html')          

def index(request):
    return  render_to_response('index.html')  