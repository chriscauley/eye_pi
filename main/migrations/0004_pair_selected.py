# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_pair_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
