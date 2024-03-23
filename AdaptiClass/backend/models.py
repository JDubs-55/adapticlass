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


# class Section(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
#     name = models.CharField(max_length=50)
#     details = models.TextField()

#     def __str__(self):
#         return f"Section {self.name} - {self.course.name}"

# class Assignment(models.Model):
#     section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='assignments')
#     name = models.CharField(max_length=50)
#     details = models.TextField()

#     def __str__(self):
#         return f"Assignment {self.name} - {self.section.course.name}"

class Course(models.Model):
    status_choices = [('Current', 'Current'), ('Completed', 'Completed')]
    status = models.CharField(max_length=15, choices=status_choices, default='Current')
    name = models.CharField(max_length=50, null=False)
    users = models.ManyToManyField(User, blank=True)
    description = models.TextField(blank=True)
    # grade = models.ManyToManyField(Grade) -- TODO: Implement after Grade model is created
    course_image = models.URLField(max_length=300, blank=True)
    # sections = models.ManyToManyField(Section, blank = True) -- TODO: Implement after Section and Assignment models are finished

    def __str__(self):
        return str(self.id) + ' : ' + self.name
