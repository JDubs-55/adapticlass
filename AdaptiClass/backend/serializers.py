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

class AssignmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'status', 'due_date', 'created_by']

    def validate(self, data):
        course = data.get('course')
        
        # Check if the course exists
        if not Course.objects.filter(pk=course.pk).exists():
            raise serializers.ValidationError("Course does not exist.")
        
        return data


class UserAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssignment
        fields = ['id', 'user', 'assignment', 'grade', 'is_complete']
        read_only_fields = ['id']
        
    def validate(self, data):
        user = data.get('user')
        assignment = data.get('assignment')

        # Check if the user exists
        if not User.objects.filter(pk=user.pk).exists():
            raise serializers.ValidationError("User does not exist.")

        # Check if the assignment exists
        if not Assignment.objects.filter(pk=assignment.pk).exists():
            raise serializers.ValidationError("Assignment does not exist.")

        return data

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'assignment', 'title', 'type']
        read_only_fields = ['id']
    
    def validate(self, data):
        assignment = data.get('assignment')
        type_value = data.get('type')

        # Check if the assignment exists
        if not Assignment.objects.filter(pk=assignment.pk).exists():
            raise serializers.ValidationError("Assignment does not exist.")
        
        # Ensure type is valid
        if type_value not in dict(Activity.ActivityType.choices):
            raise serializers.ValidationError("Invalid activity type.")

        return data

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id', 'activity', 'user', 'is_complete', 'grade']
        read_only_fields = ['id']
        
    def validate(self, data):
        activity = data.get('activity')
        user = data.get('user')
        
        if not User.objects.filter(pk=user.pk).exists():
            raise serializers.ValidationError("User does not exist")
        
        if not Activity.objects.filter(pk=activity.pk).exists():
            raise serializers.ValidationError("Activity does not exist.")
        
        return data

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'activity', 'question', 'answer']
        read_only_fields = ['id']
        
    def validate(self, data):
        activity = data.get('activity')
        
        if not Activity.objects.filter(pk=activity.pk).exists():
            raise serializers.ValidationError("Activity does not exist.")
        
        return data

class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = ['id', 'user', 'question', 'is_answered', 'is_correct', 'user_answer']
        read_only_fields = ['id']
    
    def validate(self, data):
        user = data.get('user')
        question = data.get('question')
        user_answer = data.get('user_answer')
        is_correct = data.get('is_correct')
        
        # Check user exists
        if not User.objects.filter(pk=user.pk).exists():
            raise serializers.ValidationError("User does not exist.")
        
        # Check question exists
        if not Question.objects.filter(pk=question.pk).exists():
            raise serializers.ValidationError("Question does not exist.")
        
        if user_answer != question.answer:
            if is_correct:
                raise serializers.ValidationError("User answer is not correct, but marked as correct.")
        else:
            if not is_correct:
                raise serializers.ValidationError("User answer is correct and should be marked as correct.")
            
        return data
                
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
        fields = ['id', 'user', 'assignment', 'start', 'end', 'total_time', 'engaged_time', 'engagement_periods']
    
    def validate(self, data):
        user = data.get('user')
        assignment = data.get('assignment')
        
        # Check user exists
        if not User.objects.filter(pk=user.pk).exists():
            raise serializers.ValidationError("User does not exist.")
        
        # Check question exists
        if not Assignment.objects.filter(pk=assignment.pk).exists():
            raise serializers.ValidationError("Assignment does not exist.")
        
        return data








# Old 

# class CourseGradeSerializer(serializers.ModelSerializer):
#     auth_id = serializers.SerializerMethodField('get_auth_id')

#     def get_auth_id(self, obj):
#         return obj.auth_id.auth_id

#     class Meta:
#         model = CourseGrade
#         fields = ('auth_id', 'course_id', 'grade')
        
        
        


# class AssignmentSerializer(serializers.ModelSerializer):
#     created_by = serializers.SerializerMethodField('get_created_by')

#     def get_created_by(self, obj):
#         return obj.created_by.display_name

#     class Meta:
#         model = Assignment
#         fields = (
#         'id', 'assignment_status', 'course_id', 'title', 'due_date', 'created_by', 'description', 'completion', 'num_questions', 'answered_questions',
#         'lesson_completion', 'exercise_completion', 'quiz_completion')

# class AssignmentGradeSerializer(serializers.ModelSerializer):
#     auth_id = serializers.SerializerMethodField('get_auth_id')

#     def get_auth_id(self, obj):
#         return obj.auth_id.auth_id

#     class Meta:
#         model = AssignmentGrade
#         fields = ('auth_id', 'course_id', 'assignment_id', 'grade')


# class AssignmentQuestionSerializer(serializers.ModelSerializer):
#     auth_id = serializers.SerializerMethodField('get_auth_id')

#     def get_auth_id(self, obj):
#         return obj.auth_id.auth_id

    
#     class Meta:
#         model = AssignmentQuestion
#         fields = ('id', 'auth_id', 'assignment_id', 'question_id', 'alt_question', 'student_answer', 'answered_correctly')



# class QuestionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model =  Question
#         fields = (
#             'id', 'assignment_id', 'question', 'answer'
#         )



# class AlternateQuestionSerializer(serializers.ModelSerializer):
#     auth_id = serializers.SerializerMethodField('get_auth_id')

#     def get_auth_id(self, obj):
#         return obj.auth_id.auth_id


#     class Meta:
#         model =  AlternateQuestion
#         fields = (
#             'id', 'auth_id', 'assignment_id', 'question', 'answer'
#         )
        
        
