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
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.email


class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    instructor_image = models.URLField(max_length=300)

    def __str__(self):
        return self.email


class Course(models.Model):
    course_status_choices = [('Completed', 'Completed'), ('Current', 'Current'), ('Upcoming', 'Upcoming')]
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    status = models.CharField(max_length=20, choices=course_status_choices, default='Current')
    course_description = models.TextField()

    # You can just use User for the students and instructors
    # Just validate their roles when adding a user as a student or instructor. 
    # students = models.ManyToManyField(Student)
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE, related_name='courses_taught')

    def __str__(self):
        return self.name


class StudentEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    student_grade = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    letterGrade = models.CharField(max_length=1, null=False, default="A")

    def save(self, *args, **kwargs):
        self.letterGrade = setLetterGrade(self.student_grade)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student.email + " : " + self.course.name


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


class Assignment(models.Model):
    assignment_status_choices = [('Completed', 'Completed'), ('Current', 'Current'), ('Upcoming', 'Upcoming')]
    assignment_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=assignment_status_choices, default='Current')
    title = models.CharField(max_length=50, null=False)
    description = models.TextField()
    due_date = models.DateField()
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

    assignment_completed = [('Completed', 'Completed'), ('Incomplete', 'Incomplete')]
    lesson = models.CharField(max_length=20, choices=assignment_completed, default='Incomplete')
    exercise = models.CharField(max_length=20, choices=assignment_completed, default='Incomplete')
    assessment = models.CharField(max_length=20, choices=assignment_completed, default='Incomplete')

    def __str__(self):
        return f"Assignment {self.name} - {self.section.course.name}"


class AssignmentQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    correct_answer = models.TextField()
    question_type = models.CharField(max_length=20)

    def __str__(self):
        return f"Question {self.question_id} - {self.assignment_id.title}"

    #
    #
    # class Grade(models.Model):
    #     course = models.ForeignKey('Course', on_delete=models.CASCADE)
    #     student = models.ForeignKey('Student', on_delete=models.CASCADE)
    #     score = models.DecimalField(
    #         max_digits=5, null=False, decimal_places=2, default=100.00)
    #     letterGrade = models.CharField(
    #         max_length=1, null=False, default="A")
    #
    #     def save(self, *args, **kwargs):
    #         self.letterGrade = setLetterGrade(self.score)
    #         super().save(*args, **kwargs)
    #
    #     def __str__(self):
    #         return self.letterGrade
    #
    #
    # class Section(models.Model):
    #     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    #     name = models.CharField(max_length=50)
    #     details = models.TextField()
    #
    #     def __str__(self):
    #         return f"Section {self.name} - {self.course.name}"
