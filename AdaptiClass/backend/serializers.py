from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'auth_id', 'email', 'email_verified',
                  'auth0_name', 'display_name', 'picture', 'role')


class CourseSerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField(write_only=True)
    instructor = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'status', 'name', 'instructor_id', 'instructor', 'description', 'course_image')
        
    def create(self, validated_data):
        instructor_id = validated_data.pop('instructor_id')
        
        try:
    
            instructor = User.objects.get(id=instructor_id)
            
            if instructor.role != "instructor":
                raise serializers.ValidationError("Assigned user is not an instructor.")
            
            
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid instructor id")
        
        course = Course.objects.create(instructor=instructor, **validated_data)
        return course
        
class EnrollmentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ('id', 'user_id', 'user', 'course_id', 'course', 'grade')
        
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        course_id = validated_data.pop('course_id')
        
        # Check if the user with user_id exists
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with id {} does not exist".format(user_id))

        # Check if the course with course_id exists
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course with id {} does not exist".format(course_id))

        enrollment = Enrollment.objects.create(user=user, course=course, **validated_data)
        return enrollment







class CourseGradeSerializer(serializers.ModelSerializer):
    auth_id = serializers.SerializerMethodField('get_auth_id')

    def get_auth_id(self, obj):
        return obj.auth_id.auth_id

    class Meta:
        model = CourseGrade
        fields = ('auth_id', 'course_id', 'grade')
        
        
        


class AssignmentSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_created_by')

    def get_created_by(self, obj):
        return obj.created_by.display_name

    class Meta:
        model = Assignment
        fields = (
        'id', 'assignment_status', 'course_id', 'title', 'due_date', 'created_by', 'description', 'completion', 'num_questions', 'answered_questions',
        'lesson_completion', 'exercise_completion', 'quiz_completion')

class AssignmentGradeSerializer(serializers.ModelSerializer):
    auth_id = serializers.SerializerMethodField('get_auth_id')

    def get_auth_id(self, obj):
        return obj.auth_id.auth_id

    class Meta:
        model = AssignmentGrade
        fields = ('auth_id', 'course_id', 'assignment_id', 'grade')


class AssignmentQuestionSerializer(serializers.ModelSerializer):
    auth_id = serializers.SerializerMethodField('get_auth_id')

    def get_auth_id(self, obj):
        return obj.auth_id.auth_id

    
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
    auth_id = serializers.SerializerMethodField('get_auth_id')

    def get_auth_id(self, obj):
        return obj.auth_id.auth_id


    class Meta:
        model =  AlternateQuestion
        fields = (
            'id', 'auth_id', 'assignment_id', 'question', 'answer'
        )
        
        
# Engagement Data Serializers 
class EngagementPeriodSerializer(serializers.ModelSerializer):
    engagement_data = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = EngagementPeriod
        fields = ['id', 'engagement_data', 'state', 'start', 'end', 'duration']
    
    def create(self, validated_data):
        engagement_data = self.context['engagement_data']
        engagement_period = EngagementPeriod.objects.create(engagement_data=engagement_data, **validated_data)
        return engagement_period

class EngagementDataSerializer(serializers.ModelSerializer):
    engagement_periods = EngagementPeriodSerializer(many=True, read_only=True)

    class Meta:
        model = EngagementData
        fields = ['id', 'start', 'end', 'total_time', 'engaged_time', 'engagement_periods']
        
