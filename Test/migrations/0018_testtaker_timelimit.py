# Generated by Django 3.1.1 on 2021-07-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0017_auto_20210623_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtaker',
            name='timeLimit',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
