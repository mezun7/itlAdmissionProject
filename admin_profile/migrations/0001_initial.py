# Generated by Django 3.1.7 on 2022-03-15 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Время ошибки')),
                ('message', models.CharField(max_length=3000, verbose_name='Ошибка')),
                ('party_id', models.IntegerField(blank=True, max_length=100, null=True, verbose_name='ID текстом')),
                ('participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admission.participant', verbose_name='Участник')),
            ],
        ),
    ]
