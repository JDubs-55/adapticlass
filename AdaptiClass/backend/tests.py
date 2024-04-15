import json, uuid
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

## USER TESTS
from .serializers import UserSerializer

class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def generate_user_data(self):
        unique_id = str(uuid.uuid4())[:8]  # Generate a unique identifier
        return {
            "auth_id": unique_id,  # Generate a unique UUID for auth_id
            "email": f"test_{unique_id}@example.com",  # Unique email address
            "email_verified": True,
            "auth0_name": "Test User",
            "display_name": "Test Display Name",
            "picture": "https://example.com/test.jpg",
            "role": "Student"
        }

    def test_create_user(self):
        # Create a user correctly
        user_data = self.generate_user_data()
        url = '/users/'
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(auth_id=user_data['auth_id']).count(), 1)

    def test_get_user_list(self):
        url = '/users/'
        user_data1 = self.generate_user_data()
        response = self.client.post(url, user_data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(auth_id=user_data1['auth_id']).count(), 1)
       
        user_data2 = self.generate_user_data()
        response = self.client.post(url, user_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(auth_id=user_data2['auth_id']).count(), 1)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_detail(self):
        user_data = self.generate_user_data()
        url = '/users/'
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(auth_id=user_data['auth_id']).count(), 1)

        url = f"/users/{user_data['auth_id']}/"
        user = User.objects.get(auth_id=user_data['auth_id'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserSerializer(user).data)

    def test_update_user(self):
        user_data = self.generate_user_data()
        url = '/users/'
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(auth_id=user_data['auth_id']).count(), 1)

        user = User.objects.get(auth_id=user_data['auth_id'])
        updated_data = {
            "auth_id": user.auth_id,
            "email": f"test_{user.auth_id}@example.com",
            "email_verified": False,
            "auth0_name": "Test User",
            "display_name": "Updated Display Name",
            "picture": "https://example.com/test.jpg",
            "role": "Student"
        }
        url = f"/users/{user.auth_id}/"
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        user.refresh_from_db()
        self.assertFalse(user.email_verified)
        self.assertEqual(user.display_name, 'Updated Display Name')

    def test_delete_user(self):
        user_data = self.generate_user_data()
        url = '/users/'
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(auth_id=user_data['auth_id']).count(), 1)

        url = f"/users/{user_data['auth_id']}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_user_creation(self):
        # Use the same email address for creating two users
        user_data1 = self.generate_user_data()
        user_data2 = self.generate_user_data()
        user_data2['email'] = user_data1['email']

        url = '/users/'
        response = self.client.post(url, user_data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, user_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Use the same auth_id for creating two users
        user_data3 = self.generate_user_data()
        user_data4 = self.generate_user_data()
        user_data4['auth_id'] = user_data3['auth_id']

        url = '/users/'
        response = self.client.post(url, user_data3, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, user_data4, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create a user incorrectly (no auth_id)
        user_data5 = {
            "email": f"test_@example.com",  # Unique email address
            "email_verified": True,
            "auth0_name": "Test User",
            "display_name": "Test Display Name",
            "picture": "https://example.com/test.jpg",
            "role": "Student"
        }
        response = self.client.post(url, user_data5, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create a user incorrectly (no email)
        user_data5 = {
            "auth_id": "123456789",
            "email_verified": True,
            "auth0_name": "Test User",
            "display_name": "Test Display Name",
            "picture": "https://example.com/test.jpg",
            "role": "Student"
        }
        response = self.client.post(url, user_data5, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




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