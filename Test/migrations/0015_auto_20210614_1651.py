# Generated by Django 3.1.1 on 2021-06-14 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0014_auto_20210613_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testpackage',
            name='settings',
            field=models.JSONField(blank=True, default={'canViewScorePage': True, 'canViewScorePageAuth': False, 'completeRequired': True, 'limitByScheduleFinish': False, 'limitByScheduleStart': True, 'onlyRegistered': False, 'randomSequences': True, 'viewAnswerKey': True, 'viewDetail': True, 'viewScore': True}, null=True),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='timeFinish',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 14, 16, 51, 13, 415206), null=True),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='timeStart',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 14, 16, 51, 13, 415168), null=True),
        ),
    ]