from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('auth_id','email','email_verified','auth0_name','display_name','picture','role')
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'email')

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('id', 'name', 'email')

class GradeSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField('get_course')
    student = serializers.SerializerMethodField('get_student')

    def get_course(self, obj):
        return obj.course.name
    
    def get_student(self, obj):
        return obj.student.email

    class Meta:
        model = Grade
        fields = ('id', 'course', 'student', 'score', 'letterGrade')

class CourseSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField('get_students')
    instructor = serializers.SerializerMethodField('get_instructor')

    def get_students(self, obj):
        return [students.email for students in obj.students.all()]

    def get_instructor(self, obj):
        return obj.instructor.email

    class Meta:
        model = Course
        fields = ('id', 'name', 'students', 'instructor')
        read_only_fields = ('id', 'name')
    
    