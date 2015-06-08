# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='status',
            field=models.IntegerField(max_length=32, verbose_name='\u72b6\u6001', choices=[(1, 'Init'), (2, 'Standby'), (3, 'Online'), (4, 'Offline'), (5, 'Unreachable'), (6, 'Deprecated'), (7, 'Maintenance')]),
            preserve_default=True,
        ),
    ]
