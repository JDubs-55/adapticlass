from django.db import models
from decimal import *

# Create your models here.


class User(models.Model):
    auth_id = models.CharField(max_length=100, unique=True, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    email_verified = models.BooleanField(default=False, null=False)
    auth0_name = models.CharField(max_length=50, null=False)
    display_name = models.CharField(max_length=50, null=False)
    picture = models.URLField(max_length=300)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.auth_id + " : " + self.email


class Course(models.Model):
    status_choices = [('Current', 'Current'), ('Completed', 'Completed')]
    status = models.CharField(max_length=15, choices=status_choices, default='Current')
    name = models.CharField(max_length=50, null=False)
    users = models.ManyToManyField(User, blank=True)
    description = models.TextField(blank=True)
    # grade = models.ManyToManyField(Grade) -- TODO: Implement after Grade model is created
    course_image = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return str(self.id) + ' : ' + self.name


class Assignment(models.Model):
    assignment_status_choices = [('In Progress', 'In Progress'), ('Upcoming', 'Upcoming'), ('Past Due', 'Past Due')]
    assignment_status = models.CharField(max_length = 20, choices = assignment_status_choices, default='Upcoming')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    completion = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.00)
    num_questions = models.PositiveSmallIntegerField(default = 0)
    answered_questions = models.PositiveSmallIntegerField(default = 0)
    #grade = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    lesson_completion = models.BooleanField(default = False)
    exercise_completion = models.BooleanField(default = False)
    quiz_completion = models.BooleanField(default = False)

    def str(self):
        return str(self.id) + " : " + self.title


class Question(models.Model):
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def str(self):
        return str(self.id) + " : " + self.question

class AlternateQuestion(models.Model):
    auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def str(self):
        return str(self.id) + " : " + self.question
    
class AssignmentQuestion(models.Model):
    auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    alt_question = models.ManyToManyField(AlternateQuestion, blank=True)
    student_answer = models.TextField()
    answered_correctly = models.BooleanField(default = False)

    def str(self):
        return str(self.id) + " : " + str(self.question_id)
    
    
    
    
# Engagement Data Models
class EngagementData(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    total_time = models.FloatField()

class EngagementPeriod(models.Model):
    engagement_data = models.ForeignKey(EngagementData, on_delete=models.CASCADE, related_name='engagement_periods')
    state = models.CharField(max_length=10)
    start = models.FloatField()
    duration = models.FloatField()
    end = models.FloatField()