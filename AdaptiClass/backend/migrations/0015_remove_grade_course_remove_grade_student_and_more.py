# Generated by Django 5.0.2 on 2024-03-20 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_alter_course_sections_alter_course_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='course',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='student',
        ),
        migrations.DeleteModel(
            name='Instructor',
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]