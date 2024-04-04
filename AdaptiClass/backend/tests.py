from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
from django.utils import timezone

# Create your tests here.

# This test suite verifies the integrity of the Chat model and its relationships. 
# It checks: 1) Creation of Chat with correct attributes and foreign keys to User and Assignment.
# 2) User's association with Course. 3) Assignment's link to Course. 
# Ensures relational integrity and correct data association across User, Course, Assignment, and Chat models.
class ChatModelTest(TestCase):
    def setUp(self):
        # Create a User instance
        self.user = User.objects.create(
            auth_id="unique_auth_id",
            email="user@example.com",
            email_verified=True,
            auth0_name="auth0_username",
            display_name="User Display Name",
            picture="http://example.com/picture.jpg",
            role="Student"
        )

        # Create a Course instance
        self.course = Course.objects.create(
            name="Test Course",
            description="A test course.",
            course_image="http://example.com/course_image.jpg"
        )

        # Ensure the User is enrolled in the Course
        self.course.users.add(self.user)

        # Create an Assignment instance
        self.assignment = Assignment.objects.create(
            course_id=self.course,
            title="Test Assignment",
            due_date=timezone.now().date(),
            created_by=self.user,
            description="A test assignment.",
            completion=0.00,
            num_questions=1,
            answered_questions=0,
            lesson_completion=False,
            exercise_completion=False,
            quiz_completion=False
        )

        # Create a Chat instance
        self.chat = Chat.objects.create(
            auth_id=self.user,
            assignment_id=self.assignment,
            question="What is the meaning of life?",
            solution="42"
        )

    def test_chat_creation(self):
        """Test the Chat model can create a chat with proper foreign key relationships."""
        self.assertEqual(self.chat.question, "What is the meaning of life?")
        self.assertEqual(self.chat.solution, "42")
        self.assertEqual(self.chat.auth_id, self.user)
        self.assertEqual(self.chat.assignment_id, self.assignment)
        self.assertEqual(self.chat.assignment_id.course_id, self.course)

    def test_course_user_relation(self):
        """Test the User is correctly associated with the Course."""
        self.assertIn(self.user, self.course.users.all())

    def test_assignment_course_relation(self):
        """Test the Assignment is correctly associated with the Course."""
        self.assertEqual(self.assignment.course_id, self.course)

# ---------------------------------------------------------------------------------------------------
# The ChatbotViewTest simulates POST requests to the ChatbotView, testing response to valid and invalid input. 
# It mocks external API calls to ensure the view handles data correctly and returns appropriate responses
class ChatbotViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('chatbot_view')

    @patch('backend.views.genai.GenerativeModel.generate_content')
    def test_post_valid_question(self, mock_generate_content):
        mock_generate_content.return_value = MockResponse(parts=[MockPart(text='Mocked solution')])

        response = self.client.post(self.url, {'question': 'Sample question'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('solution', response.data)
        self.assertEqual(response.data['solution'], 'Mocked solution')

    def test_post_invalid_request(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class MockResponse:
    def __init__(self, parts=None):
        self.parts = parts or []

class MockPart:
    def __init__(self, text=''):
        self.text = text