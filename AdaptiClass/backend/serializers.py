from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('auth_id','email','email_verified','auth0_name','display_name','picture','role')
        read_only_fields = ('auth_id','email','email_verified','auth0_name','picture','role')


# Updated  serializers.py
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'details')
       


class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)  # Add this line to include sections
    students = serializers.SerializerMethodField('get_students')
    instructor = serializers.SerializerMethodField('get_instructor')
    
    def get_students(self, obj):
        return [students.auth_id for students in obj.users.all() if students.role == 'Student']

    def get_instructor(self, obj):
        return [instructor.auth_id for instructor in obj.users.all() if instructor.role == 'Instructor']
    

    def create(self, validated_data):
        # Extract sections data from validated_data
        sections_data = validated_data.pop('sections', [])

        # Create the course
        course = Course.objects.create(**validated_data)

        # Create sections associated with the course
        sections = []
        for section_data in sections_data:
            section_serializer = SectionSerializer(data=section_data)
            if section_serializer.is_valid():
                section_serializer.save(course=course)
                sections.append(section_serializer.instance)
            else:
                # If any section data is invalid, delete the created course and raise an error
                course.delete()
                raise serializers.ValidationError(section_serializer.errors)

        # Set the sections for the course
        course.sections.set(sections)
        return course

    class Meta:
        model = Course
        fields = ('id', 'name', 'students', 'instructor', 'sections')
        read_only_fields = ('id', 'name', 'sections')
    



class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'section', 'name', 'details')