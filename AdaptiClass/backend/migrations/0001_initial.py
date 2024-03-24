# Generated by Django 5.0.2 on 2024-03-24 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_status', models.CharField(choices=[('In Progress', 'In Progress'), ('Upcoming', 'Upcoming'), ('Past Due', 'Past Due')], default='Upcoming', max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('due_date', models.DateField()),
                ('description', models.TextField()),
                ('completion', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('num_questions', models.PositiveSmallIntegerField(default=0)),
                ('answered_questions', models.PositiveSmallIntegerField(default=0)),
                ('lesson_completion', models.BooleanField(default=False)),
                ('exercise_completion', models.BooleanField(default=False)),
                ('quiz_completion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Current', 'Current'), ('Completed', 'Completed')], default='Current', max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('course_image', models.URLField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_id', models.CharField(max_length=100, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('auth0_name', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=50)),
                ('picture', models.URLField(max_length=300)),
                ('role', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AlternateQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('assignment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.assignment')),
                ('auth_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.course'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('assignment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.assignment')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='users',
            field=models.ManyToManyField(blank=True, to='backend.user'),
        ),
        migrations.CreateModel(
            name='AssignmentQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_answer', models.TextField()),
                ('answered_correctly', models.BooleanField(default=False)),
                ('alt_question', models.ManyToManyField(blank=True, to='backend.alternatequestion')),
                ('assignment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.assignment')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.question')),
                ('auth_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user'),
        ),
    ]