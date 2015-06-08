# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('display_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=50)),
                ('display_name', models.CharField(unique=True, max_length=50)),
                ('ip', models.IPAddressField(unique=True)),
                ('port', models.IntegerField(default=b'22')),
                ('os', models.CharField(default=b'linux', max_length=20, verbose_name=b'Operating System')),
                ('status', models.CharField(max_length=32, verbose_name='\u72b6\u6001', choices=[(1, 'Init'), (2, 'Standby'), (3, 'Online'), (4, 'Offline'), (5, 'Unreachable'), (6, 'Deprecated'), (7, 'Maintenance')])),
                ('poll_interval', models.IntegerField(default=300)),
                ('group', models.ManyToManyField(to='web.Group', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u4efb\u52a1\u540d\u79f0')),
                ('description', models.TextField(null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('task_type', models.CharField(max_length=32, verbose_name='\u4efb\u52a1\u7c7b\u578b', choices=[(b'cmd', b'\xe5\x91\xbd\xe4\xbb\xa4\xe6\x89\xa7\xe8\xa1\x8c'), (b'file_transfer', b'\xe6\x96\x87\xe4\xbb\xb6\xe5\x88\x86\xe5\x8f\x91'), (b'config_allocation', b'\xe9\x85\x8d\xe7\xbd\xae\xe4\xb8\x8b\xe5\x8f\x91')])),
                ('content', models.TextField(verbose_name='\u4efb\u52a1\u5185\u5bb9')),
                ('kick_off_at', models.DateTimeField(null=True, verbose_name='\u6267\u884c\u65f6\u95f4', blank=True)),
                ('memo', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.CharField(max_length=32, verbose_name='\u7ed3\u679c', choices=[(b'success', '\u6210\u529f'), (b'failed', '\u5931\u8d25'), (b'unknown', '\u672a\u77e5')])),
                ('log', models.TextField(verbose_name='\u4efb\u52a1\u65e5\u5fd7')),
                ('host_id', models.IntegerField(default=None, verbose_name='\u6c47\u62a5\u4e3b\u673aID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('task', models.ForeignKey(to='web.TaskCenter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='taskcenter',
            name='created_by',
            field=models.ForeignKey(verbose_name='\u4efb\u52a1\u521b\u5efa\u8005', blank=True, to='web.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskcenter',
            name='groups',
            field=models.ManyToManyField(default=None, to='web.Group', verbose_name='\u9009\u62e9\u7ec4'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskcenter',
            name='hosts',
            field=models.ManyToManyField(default=None, to='web.Host', verbose_name='\u9009\u62e9\u4efb\u52a1\u4e3b\u673a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(blank=True, to='web.Idc', null=True),
            preserve_default=True,
        ),
    ]
