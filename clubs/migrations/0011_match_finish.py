# Generated by Django 4.1 on 2022-08-31 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0010_result_matches_alter_result_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='finish',
            field=models.BooleanField(default=False),
        ),
    ]
