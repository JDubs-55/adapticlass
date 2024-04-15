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
        return self.auth_id + " : " + self.email + " : " + self.display_name
    

class Course(models.Model):
    
    class Status(models.TextChoices):
        CURRENT = 'Current'
        COMPLETED = 'Completed'
        
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CURRENT)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course", default=1)
    course_image = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return str(self.id) + ' : ' + self.name

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.user.display_name + " : [" + str(self.course.name) + " : " + str(self.grade) + "]"

class Assignment(models.Model):
    
    class Status(models.TextChoices):
        IN_PROGRESS = 'In Progress'
        UPCOMING = 'Upcoming'
        COMPLETED = 'Completed'
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField()
    status = models.CharField(max_length = 20, choices = Status.choices, default=Status.UPCOMING)
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + " : " + self.title
    
class UserAssignment(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_complete = models.BooleanField(default = False)

    def __str__(self):
        return self.user.display_name + " : [" + str(self.assignment.title) + " : " + str(self.grade) + "]"

class Activity(models.Model):
            
    class ActivityType(models.TextChoices):
        LESSON = 'Lesson'
        EXERCISE = 'Exercise'
        ASSESSMENT = 'Assessment'
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    type = models.CharField(max_length=10, choices=ActivityType.choices, default=ActivityType.EXERCISE)
    
    def __str__(self):
        return self.assignment.title + " : " + self.type

class UserActivity(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    def __str__(self):
        return self.activity.title + " : " + str(self.grade)
    

class Question(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_answered = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)
    user_answer = models.TextField(default="")
    

class Chat(models.Model):
    auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.TextField()
    solution = models.TextField()

    def __str__(self):
        return str(self.id) + " : " + self.solution
    

# Engagement Data Models
class EngagementData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    total_time = models.FloatField()
    engaged_time = models.FloatField(default=0)

class EngagementPeriod(models.Model):
    engagement_data = models.ForeignKey(EngagementData, on_delete=models.CASCADE, related_name='engagement_periods')
    state = models.CharField(max_length=10)
    start = models.FloatField()
    duration = models.FloatField()
    end = models.FloatField()




##OLD

# class CourseGrade(models.Model):
#     auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
#     grade = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

#     def __str__(self):
#         return self.auth_id.auth_id + " : [" + str(self.course_id) + " : " + str(self.grade) + "]"


# class Assignment(models.Model):
#     assignment_status_choices = [('In Progress', 'In Progress'), ('Upcoming', 'Upcoming'), ('Past Due', 'Past Due')]
#     assignment_status = models.CharField(max_length = 20, choices = assignment_status_choices, default='Upcoming')
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100, null=False)
#     due_date = models.DateField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     description = models.TextField()
#     completion = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.00)
#     num_questions = models.PositiveSmallIntegerField(default = 0)
#     answered_questions = models.PositiveSmallIntegerField(default = 0)
#     lesson_completion = models.BooleanField(default = False)
#     exercise_completion = models.BooleanField(default = False)
#     quiz_completion = models.BooleanField(default = False)

#     def __str__(self):
#         return str(self.id) + " : " + self.title
    
# class AssignmentGrade(models.Model):
#     auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
#     assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     grade = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

#     def __str__(self):
#         return self.auth_id.auth_id + " : [" + str(self.assignment_id) + " : " + str(self.grade) + "]"


# class Question(models.Model):
#     assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     question = models.TextField()
#     answer = models.TextField()

#     def __str__(self):
#         return str(self.id) + " : " + self.question

# class AlternateQuestion(models.Model):
#     auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     question = models.TextField()
#     answer = models.TextField()

#     def __str__(self):
#         return str(self.id) + " : " + self.question
    
# class AssignmentQuestion(models.Model):
#     auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
#     alt_question = models.ManyToManyField(AlternateQuestion, blank=True)
#     student_answer = models.TextField()
#     answered_correctly = models.BooleanField(default = False)

#     def __str__(self):
#         return str(self.id) + " : " + str(self.question_id)
    

