# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20150421_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcenter',
            name='file',
            field=models.FileField(upload_to=b'./upload/', null=True, verbose_name='\u4e0a\u4f20\u6587\u4ef6', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskcenter',
            name='is_template',
            field=models.BooleanField(default=False, verbose_name='\u5b58\u4e3a\u4efb\u52a1\u6a21\u7248'),
            preserve_default=True,
        ),
    ]
