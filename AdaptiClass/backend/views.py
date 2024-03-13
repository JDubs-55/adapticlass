from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . serializers import *
from . models import *

# Create your views here.
class UserListView(APIView):
    # Really for Debugging, not really needed for the app at this point. 
    # Will need something like this in the future, but will need to filter on role="student"
    # But its probably easier to just get that from the course. 
    def get(self, request):
        users = User.objects.filter()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def post(self, request):
        data = {
            "auth_id": request.data.get("auth_id"),
            "email": request.data.get("email"), 
            "email_verified": request.data.get("email_verified"),
            "auth0_name": request.data.get("auth0_name"),
            "display_name": request.data.get("display_name"),
            "picture": request.data.get("picture"),
            "role": request.data.get("role"),
        }
        
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):

    def get_object(self, user_id):
        try:
            return User.objects.get(auth_id = user_id)
        except User.DoesNotExist:
            return None
        
    #Get request 200 found, 404 not found
    def get(self, request, user_id):
        user_instance = self.get_object(user_id)
        
        if not user_instance:
            return Response(
                {"res": "Object with that user_id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Post request 201 created, 400 data invalid
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StudentListView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if email:
            try:
                student = Student.objects.get(email=email)
                serializer = StudentSerializer(student)
                # return Response(serializer.data)
                return redirect('student_detail_view', pk=student.pk)
            except Student.DoesNotExist:
                return Response({"error": "Student not found"}, status=404)   
        else:                     
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
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('student_detail_view', pk=pk)  # Redirect to GET view of the same student
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return Response({"message": f"Student '{student.email}' deleted"}, status=status.HTTP_204_NO_CONTENT)


class InstructorListView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if email:
            try:
                instructor = Instructor.objects.get(email=email)
                serializer = InstructorSerializer(instructor)
                # return Response(serializer.data)
                return redirect('instructor_detail_view', pk=instructor.pk)
            except Instructor.DoesNotExist:
                return Response({"error": "Instructor not found"}, status=404)   
        else:                     
            instructors = Instructor.objects.all()
            serializer = InstructorSerializer(instructors, many=True)
            return Response(serializer.data)
 
    def post(self, request):
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InstructorDetailView(APIView):
    def get(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)

    def put(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        serializer = InstructorSerializer(instructor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('instructor_detail_view', pk=pk)  # Redirect to GET view of the same instructor
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        instructor.delete()
        return Response({"message": f"Instructor '{instructor.email}' deleted"}, status=status.HTTP_204_NO_CONTENT)


class CourseListView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        if name:
            try:
                course = Course.objects.get(name=name)
                serializer = InstructorSerializer(course)
                # return Response(serializer.data)
                return redirect('course_detail_view', pk=course.pk)
            except Instructor.DoesNotExist:
                return Response({"error": "Instructor not found"}, status=404)   
        else:                     
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView): 
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            new_name = request.data.get('name')
            if new_name:
                course.name = new_name

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
            serializer.save()
            return redirect('course_detail_view', pk=pk)  # Redirect to GET view of the same course
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response({"message": f"Course '{course.name}' deleted"}, status=status.HTTP_204_NO_CONTENT)

class RemoveStudentsFromCourseView(APIView):
    # def get_object(self, name):
    #     try:
    #         return Course.objects.get(name=name)
    #     except Course.DoesNotExist:
    #         raise Http404("Course does not exist")
        
    # def get(self, request, name):
    #     course = self.get_object(name)
    #     serializer = CourseSerializer(course)
    #     return Response(serializer.data)
    
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
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
                remove_messages.append(f"Student '{email}' removed from course '{course.name}'")
            except Student.DoesNotExist:
                error_messages.append(f"Student '{email}' not found")

        # Construct response message
        message = {
            "message": remove_messages,
            "errors": error_messages
        }

        return Response(message, status=status.HTTP_200_OK)