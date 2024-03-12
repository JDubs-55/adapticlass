from django.shortcuts import render
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . serializers import *
from . models import *
from django.shortcuts import get_object_or_404

# Create your views here.
class StudentListView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentDetailView(APIView):
    def get_object(self, email):
        try:
            return Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise Http404("Student does not exist")
        
    def get(self, request, email):
        student = self.get_object(email)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, email):
        student = self.get_object(email)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, email):
        student = self.get_object(email)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class InstructorListView(APIView):
    def get(self, request):
        instructor = Instructor.objects.all()
        serializer = InstructorSerializer(instructor, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InstructorDetailView(APIView):
    def get_object(self, email):
        try:
            return Instructor.objects.get(email=email)
        except Instructor.DoesNotExist:
            raise Http404("Instructor does not exist")
        
    def get(self, request, email):
        instructor = self.get_object(email)
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)
    
    def put(self, request, email):
        instructor = self.get_object(email)
        serializer = InstructorSerializer(instructor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, email):
        instructor = self.get_object(email)
        instructor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get('name')
            instructor_email = request.data.get('instructor')
            if not instructor_email:
                return Response({"error": "Instructor email is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                instructor = Instructor.objects.get(email=instructor_email)
            except Instructor.DoesNotExist:
                return Response({"error": "Instructor not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(name=name,instructor=instructor)


            # Handle sections
            if 'sections' in request.data:
                sections_data = request.data['sections']
                section_serializer = SectionSerializer(data=sections_data, many=True)
                
                try:
                    if section_serializer.is_valid():
                        # Save the sections associated with the course
                        sections = section_serializer.save(course=serializer.instance)
                        # Associate the saved sections with the course
                        serializer.instance.sections.set(sections)
                    else:
                        return Response(section_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):
    def get_object(self, name):
        try:
            return Course.objects.get(name=name)
        except Course.DoesNotExist:
            raise Http404("Course does not exist")

    def get(self, request, name):
        course = self.get_object(name)
        serializer = CourseSerializer(course)
        return Response(serializer.data)


    def put(self, request, name):
        course = self.get_object(name)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            # Check if 'instructor' field is present in the request data
            if 'instructor' in request.data:
                instructor_email = request.data['instructor']
                try:
                    instructor = Instructor.objects.get(email=instructor_email)
                except Instructor.DoesNotExist:
                    return Response({"error": "Instructor not found"}, status=status.HTTP_404_NOT_FOUND)
                course.instructor = instructor
            # Check if 'students' field is present in the request data
            if 'students' in request.data:
                student_emails = request.data['students']
                if isinstance(student_emails, str):  # If a single student email is provided
                    student_emails = [student_emails]  # Convert it to a list for consistency
                    
                for student_email in student_emails:
                    try:
                        student = Student.objects.get(email=student_email)
                    except Student.DoesNotExist:
                        return Response({"error": f"Student '{student_email}' not found"}, status=status.HTTP_404_NOT_FOUND)
                    course.students.add(student)

            # Handle sections
            if 'sections' in request.data:
                sections_data = request.data['sections']
                for section_data in sections_data:
                    # Remove the 'course' field from each section data
                    if 'course' in section_data:
                        del section_data['course']
                section_serializer = SectionSerializer(data=sections_data, many=True)
                if section_serializer.is_valid():
                    sections = section_serializer.save(course=course)
                    serializer.instance.sections.set(sections)
                else:
                    return Response(section_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            serializer.save()

        

                        
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        course = self.get_object(name)
        course.delete()
        return Response({"message": f"Course '{name}' deleted"}, status=status.HTTP_204_NO_CONTENT)

# class AddStudentToCourseView(APIView):
#     def put(self, request, name):
#         try:
#             course = Course.objects.get(name=name)
#         except Course.DoesNotExist:
#             return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

#         email = request.data.get('email', None)
#         if not email:
#             return Response({"error": "Email of the student to be added is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             student = Student.objects.get(email=email)
#         except Student.DoesNotExist:
#             return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

#         course.students.add(student)
#         return Response({"message": f"Student '{email}' added to course '{name}'"}, status=status.HTTP_200_OK)

class RemoveStudentsFromCourseView(APIView):
    def get_object(self, name):
        try:
            return Course.objects.get(name=name)
        except Course.DoesNotExist:
            raise Http404("Course does not exist")
        
    def get(self, request, name):
        course = self.get_object(name)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, name):
        try:
            course = Course.objects.get(name=name)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the email(s) to remove
        emails = request.data['students']
        if not emails:
            return Response({"error": "Email(s) of the student(s) to be removed is required"}, status=status.HTTP_400_BAD_REQUEST)

        # If a single email is provided, convert it to a list
        if isinstance(emails, str):
            emails = [emails]

        remove_messages = []
        error_messages = []

        # Iterate over each email and remove the corresponding student
        for email in emails:
            try:
                student = Student.objects.get(email=email)
                course.students.remove(student)
                remove_messages.append(f"Student '{email}' removed from course '{name}'")
            except Student.DoesNotExist:
                error_messages.append(f"Student '{email}' not found")

        # Construct response message
        message = {
            "message": remove_messages,
            "errors": error_messages
        }

        return Response(message, status=status.HTTP_200_OK)
    





#sections and assignments view 


class SectionDetailView(APIView):
    def get_object(self, course_id, section_id):
        try:
            return Section.objects.get(course_id=course_id, id=section_id)
        except Section.DoesNotExist:
            raise Http404("Section does not exist")

    def get(self, request, course_id, section_id):
        section = self.get_object(course_id, section_id)
        serializer = SectionSerializer(section)
        return Response(serializer.data)

    def put(self, request, course_id, section_id):
        section = self.get_object(course_id, section_id)
        serializer = SectionSerializer(section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentDetailView(APIView):
    def get_object(self, section_id, assignment_id):
        try:
            return Assignment.objects.get(section_id=section_id, id=assignment_id)
        except Assignment.DoesNotExist:
            raise Http404("Assignment does not exist")

    def get(self, request, section_id, assignment_id):
        assignment = self.get_object(section_id, assignment_id)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    def put(self, request, section_id, assignment_id):
        assignment = self.get_object(section_id, assignment_id)
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)