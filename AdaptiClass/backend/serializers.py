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



class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
        'id', 'assignment_status', 'title', 'due_date', 'created_by', 'description', 'completion', 'num_questions', 'answered_questions',
        'lesson_completion', 'exercise_completion', 'quiz_completion')


class AssignmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentQuestion
        fields = ('id', 'auth_id', 'assignment_id', 'question_id', 'alt_question', 'student_answer', 'answered_correctly')



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Question
        fields = (
            'id', 'assignment_id', 'question', 'answer'
        )



class AlternateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model =  AlternateQuestion
        fields = (
            'id', 'auth_id', 'assignment_id', 'question', 'answer'
        )