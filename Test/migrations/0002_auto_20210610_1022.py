# Generated by Django 3.1.1 on 2021-06-10 03:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testtaker',
            name='timeFinish',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 10, 10, 22, 51, 327280), null=True),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='timeStart',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 10, 10, 22, 51, 327250), null=True),
        ),
    ]
