# Generated by Django 5.0.2 on 2024-03-03 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_grade_lettergrade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='courseName',
            new_name='name',
        ),
    ]
