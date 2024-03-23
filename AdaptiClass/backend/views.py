from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . serializers import *
from . models import *
from django.shortcuts import get_object_or_404
import google.generativeai as genai

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
            return User.objects.get(auth_id=user_id)
        except User.DoesNotExist:
            return None

    # Get request 200 found, 404 not found
    def get(self, request, user_id):
        user_instance = self.get_object(user_id)

        if not user_instance:
            return Response(
                {"res": "Object with that user_id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Post request 201 created, 400 data invalid
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        user = get_object_or_404(User, auth_id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, auth_id=user_id)
        user.delete()
        return Response({"message": f"User '{user_id}' deleted"}, status=status.HTTP_204_NO_CONTENT)


class CourseListView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        if name:
            try:
                course = Course.objects.get(name=name)
                serializer = CourseSerializer(course)
                return redirect('course_detail_view', pk=course.pk)
            except Course.DoesNotExist:
                return Response({"error": "Course not found"}, status=404)
        else:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get('name')
            serializer.save(name=name)

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
            if 'name' in request.data:
                new_name = request.data.get('name')
                course.name = new_name

            if 'status' in request.data:
                new_status = request.data.get('status')
                course.status = new_status

            if 'users' in request.data:
                user_id = request.data['users']
                try:
                    user = User.objects.get(auth_id=user_id)
                except User.DoesNotExist:
                    return Response({"error": f"User '{user_id}' not found"}, status=status.HTTP_404_NOT_FOUND)
                if user.role == 'Instructor' or user.role == 'Student':
                    course.users.add(user)
                else:
                    return Response({"error": f"User '{user_id}' does not have a role"}, status=status.HTTP_400_BAD_REQUEST)

            if 'description' in request.data:
                new_description = request.data.get('description')
                course.description = new_description

            # TODO: Implement grade functionality here to update grade based on average of assignment scores

            if 'course_image' in request.data:
                new_course_image = request.data.get('course_image')
                course.course_image = new_course_image

            # TODO: Implement adding sections to courses here

            # Handle sections
            # if 'sections' in request.data:
            #     sections_data = request.data['sections']
            #     for section_data in sections_data:
            #         # Remove the 'course' field from each section data
            #         if 'course' in section_data:
            #             del section_data['course']
            #     section_serializer = SectionSerializer(data=sections_data, many=True)
            #     if section_serializer.is_valid():
            #         sections = section_serializer.save(course=course)
            #         serializer.instance.sections.set(sections)
            #     else:
            #         return Response(section_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response({"message": f"Course '{course.name}' deleted"}, status=status.HTTP_204_NO_CONTENT)


class RemoveUsersFromCourseView(APIView):
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
        user_ids = request.data['users']
        if not user_ids:
            return Response({"error": "ID(s) of the user(s) to be removed is required"}, status=status.HTTP_400_BAD_REQUEST)

        # If a single email is provided, convert it to a list
        if isinstance(user_ids, str):
            user_ids = [user_ids]

        remove_messages = []
        error_messages = []

        # Iterate over each email and remove the corresponding student
        for user_id in user_ids:
            try:
                user = User.objects.get(auth_id=user_id)
                course.users.remove(user)
                remove_messages.append(
                    f"User '{user_id}' removed from course '{course.name}'")
            except User.DoesNotExist:
                error_messages.append(f"User '{user_id}' not found")

        # Construct response message
        message = {
            "message": remove_messages,
            "errors": error_messages
        }

        return Response(message, status=status.HTTP_200_OK)


# sections and assignments view


# class SectionDetailView(APIView):
#     def get_object(self, course_id, section_id):
#         try:
#             return Section.objects.get(course_id=course_id, id=section_id)
#         except Section.DoesNotExist:
#             raise Http404("Section does not exist")

#     def get(self, request, course_id, section_id):
#         section = self.get_object(course_id, section_id)
#         serializer = SectionSerializer(section)
#         return Response(serializer.data)

#     def put(self, request, course_id, section_id):
#         section = self.get_object(course_id, section_id)
#         serializer = SectionSerializer(section, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AssignmentDetailView(APIView):
#     def get_object(self, section_id, assignment_id):
#         try:
#             return Assignment.objects.get(section_id=section_id, id=assignment_id)
#         except Assignment.DoesNotExist:
#             raise Http404("Assignment does not exist")

#     def get(self, request, section_id, assignment_id):
#         assignment = self.get_object(section_id, assignment_id)
#         serializer = AssignmentSerializer(assignment)
#         return Response(serializer.data)

#     def put(self, request, section_id, assignment_id):
#         assignment = self.get_object(section_id, assignment_id)
#         serializer = AssignmentSerializer(assignment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Updated views.py
# class SectionListView(APIView):
#     def get(self, request, course_name):
#         # Retrieve sections for the specified course
#         sections = Section.objects.filter(course__name=course_name)
#         serializer = SectionSerializer(sections, many=True)
#         return Response(serializer.data)

#     def post(self, request, course_name):
#         # Create a new section under the specified course
#         data = request.data.copy()
#         data['course'] = course_name  # Assign the course name to the section
#         serializer = SectionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AssignmentListView(APIView):
#     def post(self, request):
#         section_id = request.data.get('section')
#         if not section_id:
#             return Response({"error": "Section ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             section = Section.objects.get(id=section_id)
#         except Section.DoesNotExist:
#             return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the user making the request is associated with the course as an instructor
#         if request.user.instructor.courses.filter(id=section.course.id).exists():
#             serializer = AssignmentSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "You do not have permission to create assignments for this section"}, status=status.HTTP_403_FORBIDDEN)


class ChatbotView(APIView):
    def post(self, request):
        chat_prompt = request.data.get('problem')

        genai.configure(api_key="AIzaSyBIKvpvW6-RDwXMorDKCs-EJv8bBgmYxPo")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
        ]
        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        directions = "For the given Algebra 1 problem, illustrate each step towards finding the solution. Provide a concise text explanation for what each step accomplishes, aiming for clarity and brevity. It's crucial to demonstrate the process without skipping directly to the solution. If the following problem is not related to Math, please respond kindly prompting the student to stay on topic. Problem: "
        full_prompt = directions + chat_prompt
        prompt_parts = [{"text": full_prompt}]
        response = model.generate_content(prompt_parts)

        if response.parts:
            return Response({'solution': response.parts[0].text}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No response generated or the prompt was blocked.'},
                            status=status.HTTP_400_BAD_REQUEST)
