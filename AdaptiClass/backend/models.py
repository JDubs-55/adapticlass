from django.db import models
from decimal import *

# Create your models here.
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
