# Generated by Django 3.1.1 on 2021-01-01 06:22

import Test.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0012_auto_20210101_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questID',
            field=models.CharField(default='45ec8684800cdb85', max_length=16),
        ),
        migrations.AlterField(
            model_name='question',
            name='questionNum',
            field=models.IntegerField(default=Test.models.Question.questionNum),
        ),
        migrations.AlterField(
            model_name='testpackage',
            name='testID',
            field=models.CharField(default='02f1f8cb794ab45f', max_length=16),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='testTakerID',
            field=models.CharField(default='219d8dec7c54712b', max_length=16),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='timeFinish',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 1, 13, 22, 8, 340855), null=True),
        ),
        migrations.AlterField(
            model_name='testtaker',
            name='timeStart',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 1, 13, 22, 8, 340818), null=True),
        ),
    ]