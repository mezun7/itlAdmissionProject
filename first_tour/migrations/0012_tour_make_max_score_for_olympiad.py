# Generated by Django 3.1.7 on 2025-04-11 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_tour', '0011_tour_allways_show_id_in_final_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='make_max_score_for_olympiad',
            field=models.BooleanField(default=True, verbose_name='Максимизировать баллы олимпиадникам?'),
        ),
    ]
