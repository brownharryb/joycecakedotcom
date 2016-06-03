# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-28 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20160527_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='country',
            field=models.CharField(default='Nigeria', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='state',
            field=models.CharField(default='Rivers', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usertransaction',
            name='transaction_id_string',
            field=models.CharField(editable=False, max_length=30, unique=True),
        ),
    ]