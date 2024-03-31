from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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

            serializer.save()

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


class AssignmentListView(APIView):
    def get(self, request):
        course_name = request.query_params.get('course_name')
        if course_name:
            try:
                course = Course.objects.get(name=course_name)
                assignments = Assignment.objects.filter(course_id=course)
                serializer = AssignmentSerializer(assignments, many=True)
                url = reverse('course_assignment_view', kwargs={'course_name': course_name})
                return redirect(url)
            except Course.DoesNotExist:
                return Response({"error": "Course not found"}, status=404)
        else:
            assignments = Assignment.objects.all()
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentDetailView(APIView):
    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    def put(self, request, pk):

        assignment = get_object_or_404(Assignment, pk=pk)

        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        assignment = get_object_or_404(Assignment, pk=pk)
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CourseAssignmentListView(APIView):
    def get(self, request, course_name):
        course = get_object_or_404(Course, name=course_name)
        assignments = Assignment.objects.filter(course_id=course)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

class AssignmentQuestionListView(APIView):

    def get(self, request):
        assignments_questions = AssignmentQuestion.objects.all()
        serializer = AssignmentQuestionSerializer(
            assignments_questions, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = AssignmentQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentQuestionDetailView(APIView):

    def get(self, request, pk):
        assignments_questions = get_object_or_404(AssignmentQuestion, pk=pk)
        serializer = AssignmentQuestionSerializer(assignments_questions)
        return Response(serializer.data)

    def put(self, request, pk):

        assignments_questions = get_object_or_404(AssignmentQuestion, pk=pk)

        serializer = AssignmentQuestionSerializer(
            assignments_questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        assignments_questions = get_object_or_404(AssignmentQuestion, pk=pk)
        assignments_questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionListView(APIView):

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):

    def get(self, request, pk):
        questions = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(questions)
        return Response(serializer.data)

    def put(self, request, pk):

        questions = get_object_or_404(Question, pk=pk)

        serializer = QuestionSerializer(questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        questions = get_object_or_404(Question, pk=pk)
        questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlternateQuestionListView(APIView):

    def get(self, request):
        alt_questions = AlternateQuestion.objects.all()
        serializer = AlternateQuestionSerializer(alt_questions, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = AlternateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlternateQuestionDetailView(APIView):

    def get(self, request, pk):
        alt_questions = get_object_or_404(AlternateQuestion, pk=pk)
        serializer = AlternateQuestionSerializer(alt_questions)
        return Response(serializer.data)

    def put(self, request, pk):

        alt_questions = get_object_or_404(AlternateQuestion, pk=pk)

        serializer = AlternateQuestionSerializer(
            alt_questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        alt_questions = get_object_or_404(AlternateQuestion, pk=pk)
        alt_questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChatbotView(APIView):
    def post(self, request):
        chat_prompt = request.data.get('question')

        if chat_prompt is None:
            return Response({'error': 'Question is required.'}, status=status.HTTP_400_BAD_REQUEST)

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
        
class ProblemGeneratorView(APIView):
    def post(self, request):
        chat_prompt = request.data.get('question')
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
        directions = "For the given Algebra 1 problem, provide one similar but different problem with the same type, format, and difficulty. give the problem and the answer. they should be clearly labled Problem: put_problem_here Answer: put_answer_here. If the current problem is not related to math, respond with the word 'No' and nothing else - I need this for error handling. Current Problem: "
        full_prompt = directions + chat_prompt
        prompt_parts = [{"text": full_prompt}]
        response = model.generate_content(prompt_parts)
        
        if response.parts:
            response_text = response.parts[0].text
            if response_text == "No":
                return Response({'error': 'The provided problem is not related to Algebra 1.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                problem_start = response_text.find("Problem: ") + len("Problem: ")
                answer_start = response_text.find("Answer: ") + len("Answer: ")
                if problem_start > len("Problem: ") - 1 and answer_start > len("Answer: ") - 1:
                    problem_end = response_text.find("Answer: ") - 1
                    answer_end = len(response_text)
                    problem = response_text[problem_start:problem_end].strip()
                    answer = response_text[answer_start:answer_end].strip()
                    return Response({'question': problem, 'answer': answer}, status=status.HTTP_200_OK)
                else:
                    raise ValueError('Parsing error')
            except ValueError:
                return Response({'error': 'Error parsing the response.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No response generated or the prompt was blocked.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
