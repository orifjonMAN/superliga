# Generated by Django 4.1 on 2022-08-30 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_alter_match_match_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='club1_goals',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='club2_goals',
            field=models.IntegerField(default=0),
        ),
    ]
