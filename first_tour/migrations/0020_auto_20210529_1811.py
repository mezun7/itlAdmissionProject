# Generated by Django 3.1.7 on 2021-05-29 18:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_tour', '0019_auto_20210524_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userappeal',
            name='appeal_apply_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 29, 18, 11, 5, 52359), verbose_name='Время подачи заявления'),
        ),
    ]