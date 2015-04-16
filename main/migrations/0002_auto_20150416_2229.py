# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pair',
            name='l_axis',
            field=models.IntegerField(null=True, verbose_name=b'Left Axis', blank=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='l_cyl',
            field=models.FloatField(null=True, verbose_name=b'Left Cylinder', blank=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='l_sph',
            field=models.FloatField(null=True, verbose_name=b'Left Sphere', blank=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='r_axis',
            field=models.IntegerField(null=True, verbose_name=b'Right Axis', blank=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='r_cyl',
            field=models.FloatField(null=True, verbose_name=b'Right Cylinder', blank=True),
        ),
        migrations.AlterField(
            model_name='pair',
            name='r_sph',
            field=models.FloatField(null=True, verbose_name=b'Right Sphere', blank=True),
        ),
    ]
