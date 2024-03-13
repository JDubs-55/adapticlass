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
    
class Student(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)

   

    def __str__(self):
        return self.email

class Instructor(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)

   

    def __str__(self):
        return self.email

class Course(models.Model):
    name = models.CharField(max_length=50, null=False)
    
    # You can just use User for the students and instructors
    # Just validate their roles when adding a user as a student or instructor. 
    students = models.ManyToManyField(Student)
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def setLetterGrade(score):
    if score >= Decimal('90.00'):
        letterGrade = 'A'
    elif score >= Decimal('80.00'):
        letterGrade = 'B'
    elif score >= Decimal('70.00'):
        letterGrade = 'C'
    elif score >= Decimal('60.00'):
        letterGrade = 'D'
    else:
        letterGrade = 'F'

    return letterGrade

class Grade(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    score = models.DecimalField(
        max_digits=5, null=False, decimal_places=2, default=100.00)
    letterGrade = models.CharField(
        max_length=1, null=False, default="A")
    
    def save(self, *args, **kwargs):
        self.letterGrade = setLetterGrade(self.score)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.letterGrade





class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50)
    details = models.TextField()

    def __str__(self):
        return f"Section {self.name} - {self.course.name}"

class Assignment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='assignments')
    name = models.CharField(max_length=50)
    details = models.TextField()

    def __str__(self):
        return f"Assignment {self.name} - {self.section.course.name}"