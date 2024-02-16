from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

# User
    # name
    # email
    # password

# Student extend User
    # grade
    # engagement score
    # status
    # course

# Instructor extends User
    # courses (from Course class)
    # students (from student class) -- redundant?

# Course
    # course name
    # units (from unit class)
    # assessments (from assessment class)
    # students (from student class)

# Unit
    # unit_num
    # sections -- key/value pair {section_num : content}
        # could be lengthy, make section class?

# Assessment
    # assesment_num (corresponding to unit section)
    # questions

