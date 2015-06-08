from django import forms
from django.contrib import admin
import models





class HostAdmin(admin.ModelAdmin):
    list_display = ('id','display_name','hostname','ip','port','idc','status')



class TaskCenterAdmin(admin.ModelAdmin):
    list_display= ('id','name','task_type','content','kick_off_at','created_by','is_template')
class TaskLogAdmin(admin.ModelAdmin):
    list_display= ('task','result','date')
    readonly_fields = ('date',)   
    
    
admin.site.register(models.Idc)
admin.site.register(models.Host,HostAdmin)
admin.site.register(models.Group)
admin.site.register(models.UserProfile)
admin.site.register(models.TaskCenter,TaskCenterAdmin)
admin.site.register(models.TaskLog,TaskLogAdmin)

