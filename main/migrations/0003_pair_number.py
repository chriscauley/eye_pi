# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150416_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
