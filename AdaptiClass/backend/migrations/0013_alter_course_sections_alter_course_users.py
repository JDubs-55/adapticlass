# Generated by Django 5.0.2 on 2024-03-20 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_remove_section_course_course_sections_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='sections',
            field=models.ManyToManyField(to='backend.section'),
        ),
        migrations.AlterField(
            model_name='course',
            name='users',
            field=models.ManyToManyField(to='backend.user'),
        ),
    ]
