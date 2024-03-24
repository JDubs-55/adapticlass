from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('auth_id', 'email', 'email_verified',
                  'auth0_name', 'display_name', 'picture', 'role')
        read_only_fields = ('auth_id', 'email', 'email_verified',
                            'auth0_name', 'picture', 'role')


class CourseSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField('get_students')
    instructor = serializers.SerializerMethodField('get_instructor')

    def get_students(self, obj):
        return [students.auth_id for students in obj.users.all() if students.role == 'Student']

    def get_instructor(self, obj):
        return [instructor.display_name for instructor in obj.users.all() if instructor.role == 'Instructor']

    # TODO: Dont foget to add Grade and Section fields after creation

    class Meta:
        model = Course
        fields = ('id', 'status', 'name', 'instructor',
                  'students', 'description', 'course_image')
        read_only_fields = ('id', 'status', 'name',
                            'description', 'course_image')

class SectionSerializer(serializers.ModelSerializer):
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ('id', 'course', 'name', 'details', 'assignments')

    def get_assignments(self, obj):
        # Delayed import to avoid circular dependency
        from .serializers import AssignmentSerializer  # Adjust this import based on your project structure
        assignments = obj.assignments.all()
        return AssignmentSerializer(assignments, many=True, read_only=True).data


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
        'assignment_id', 'student_id', 'course_id', 'status', 'title', 'description', 'due_date', 'grade', 'lesson',
        'exercise', 'assessment')


class AssignmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentQuestion
        fields = ('question_id', 'assignment_id', 'question', 'answer', 'correct_answer', 'question_type')

