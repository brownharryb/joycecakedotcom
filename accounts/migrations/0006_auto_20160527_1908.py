# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-27 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160523_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertransaction',
            name='payment_medium',
            field=models.CharField(choices=[('0', 'cash on delivery'), ('1', 'interswitch'), ('2', 'paypal')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='usertransaction',
            name='session_string',
            field=models.TextField(blank=True, editable=False),
        ),
    ]
