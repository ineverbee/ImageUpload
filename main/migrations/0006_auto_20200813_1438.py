# Generated by Django 3.1 on 2020-08-13 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200813_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='height',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='width',
            field=models.IntegerField(default=None),
        ),
    ]
