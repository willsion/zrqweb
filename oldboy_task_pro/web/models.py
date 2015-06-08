#_*_coding:utf-8_*_
import sys
#reload(sys) 
#sys.setdefaultencoding("utf-8") 
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    def __unicode__(self):
        return '%s' % self.user

class Idc(models.Model):
    name=models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    display_name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.display_name

class Host(models.Model):
    hostname=models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique = True)
    ip = models.IPAddressField(unique=True)
    idc = models.ForeignKey(Idc, null=True, blank=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    port = models.IntegerField(default='22')
    os = models.CharField(max_length=20, default='linux', verbose_name='Operating System')

    status_choice = (
        (1, u'Init'), #init
        (2, u'Standby'),  #standby
        (3, u'Online'),  #online
        (4, u'Offline'),  #offline
        (5, u'Unreachable'), #unreachable
        (6, u'Deprecated'),#Deprecated'
        (7, u'Maintenance'), #Maintenance
    )
    status = models.IntegerField(u'状态',choices=status_choice,max_length=32)

    ###########for task allocation#########
    poll_interval = models.IntegerField(default=300)

    def __unicode__(self):
        return self.display_name


######################below for the task allowcation syste#############
class TaskCenter(models.Model):
    name = models.CharField(u'任务名称',max_length=128)
    description = models.TextField(u'描述',blank=True,null=True)
    created_by= models.ForeignKey('UserProfile',verbose_name=u'任务创建者',blank=True,null=True)
    task_choices = (('cmd','命令执行'),
                    ('file_transfer','文件分发'),
                    ('config_allocation','配置下发'))
    
    task_type = models.CharField(u'任务类型',choices=task_choices,max_length=32)
    hosts = models.ManyToManyField(Host, verbose_name=u'选择任务主机',default=None)
    groups = models.ManyToManyField(Group, verbose_name=u'选择组' ,default=None)
    content = models.TextField(u'任务内容')
    kick_off_at = models.DateTimeField(u'执行时间',blank=True,null=True)
    file = models.FileField(upload_to = './upload/',verbose_name=u'上传文件',blank=True,null=True)
    
    is_template = models.BooleanField(u'存为任务模版',default=False)
    memo = models.TextField(blank=True,null=True)
  
    def __unicode__(self):
        return self.name 
class TaskLog(models.Model):
    task = models.ForeignKey(TaskCenter)
    result_choices = (('success',u'成功'),
                      ('failed',u'失败'),
                      ('unknown',u'未知'))
    
    result = models.CharField(u'结果',choices=result_choices,max_length=32)
    log = models.TextField(u'任务日志')
    host_id = models.IntegerField(u'汇报主机ID',default=None)
    date = models.DateTimeField(auto_now_add=True,null=True)
    
    def __unicode__(self):
        return self.task.name 
    

