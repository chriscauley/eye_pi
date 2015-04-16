# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r_sph', models.FloatField(verbose_name=b'Right Sphere')),
                ('r_cyl', models.FloatField(verbose_name=b'Right Cylinder')),
                ('r_axis', models.IntegerField(verbose_name=b'Right Axis')),
                ('l_sph', models.FloatField(verbose_name=b'Left Sphere')),
                ('l_cyl', models.FloatField(verbose_name=b'Left Cylinder')),
                ('l_axis', models.IntegerField(verbose_name=b'Left Axis')),
                ('lens', models.CharField(max_length=32, null=True, blank=True)),
                ('frame', models.CharField(max_length=32, null=True, blank=True)),
            ],
        ),
    ]
