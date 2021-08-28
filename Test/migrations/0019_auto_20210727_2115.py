# Generated by Django 3.1.1 on 2021-07-27 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0018_testtaker_timelimit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testpackage',
            name='passwordTest',
            field=models.CharField(default=None, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='testpackage',
            name='settings',
            field=models.JSONField(blank=True, default={'allowEditData': True, 'canViewScorePage': True, 'canViewScorePageAuth': False, 'completeRequired': True, 'isActive': True, 'limitByScheduleFinish': False, 'limitByScheduleStart': True, 'onlyRegistered': False, 'randomSequences': True, 'viewAnswerKey': True, 'viewDetail': True, 'viewScore': True}, null=True),
        ),
    ]