# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-20 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160511_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='recovery_key',
            field=models.CharField(editable=False, max_length=40, null=True),
        ),
    ]
