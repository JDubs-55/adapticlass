# Generated by Django 5.0.2 on 2024-03-02 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_grade_lettergrade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='letterGrade',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
