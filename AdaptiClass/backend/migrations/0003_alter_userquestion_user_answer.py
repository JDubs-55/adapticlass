# Generated by Django 5.0.2 on 2024-04-09 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_useractivity_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestion',
            name='user_answer',
            field=models.TextField(default=''),
        ),
    ]
