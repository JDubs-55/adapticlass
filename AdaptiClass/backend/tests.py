import json, uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from datetime import datetime
from django.utils import timezone

# Create your tests here.

## USER TESTS
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


## COURSE TESTS
class CourseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user to use as an instructor
        self.instructor = User.objects.create(
            auth_id="123456789",
            email="instructor@example.com",
            email_verified=True,
            auth0_name="Instructor User",
            display_name="Instructor Display Name",
            role="instructor"
        )

    def test_create_course(self):
        url = '/courses/'
        course_data = {
            "name": "Test Course",
            "description": "Test Description",
            "status": "Current",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_course_list(self):
        url = '/courses/'
        
        # Create some courses
        course_data1 = {
            "name": "Test Course 1",
            "description": "Test Description 1",
            "status": "Current",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, course_data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        course_data2 = {
            "name": "Test Course 2",
            "description": "Test Description 2",
            "status": "Current",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, course_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_course_detail(self):
        url = '/courses/'
        course_data = {
            "name": "Test Course",
            "description": "Test Description",
            "status": "Current",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        course = Course.objects.get(name=course_data["name"])
        url = f'/courses/{course.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], course_data['name'])
        self.assertEqual(response.data['description'], course_data['description'])
        self.assertEqual(response.data['status'], course_data['status'])
        self.assertEqual(response.data['instructor']['auth_id'], self.instructor.auth_id)

    def test_update_course(self):
        url = '/courses/'
        course_data = {
            "name": "Test Course",
            "description": "Test Description",
            "status": "Current",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        course = Course.objects.get(name=course_data["name"])
        url = f'/courses/{course.id}/'
        updated_data = {
            "name": "Updated Course Name",
            "description": "Updated Description",
            "status": "Completed",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/updated_course.jpg"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.name, updated_data['name'])
        self.assertEqual(course.description, updated_data['description'])
        self.assertEqual(course.status, updated_data['status'])

    def test_delete_course(self):
        url = '/courses/'
        course_data = {
            "name": "Test Course",
            "description": "Test Description",
            "status": "Current",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        course = Course.objects.get(name=course_data["name"])
        url = f'/courses/{course.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_invalid_course_creation(self):
        # Trying to create a course with no name
        url = '/courses/'
        data = {
            "description": "Test Description",
            "status": "Current",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Trying to create a course with no instructor
        data = {
            "name": "Test Course",
            "description": "Test Description",
            "status": "Current",
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Trying to create a course with an invalid instructor ID
        data = {
            "name": "Test Course",
            "description": "Test Description",
            "status": "Current",
            "instructor_id": "987654321",
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Trying to create a course with an invalid status choice
        data = {
            "name": "Test Course",
            "description": "Test Description",
            "status": "Wrong Status",
            "instructor_id": self.instructor.id,
            "course_image": "https://example.com/course.jpg"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

## ENROLLMENT TESTS
class EnrollmentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a student user
        self.student = User.objects.create(
            auth_id="123456789",
            email="test@example.com",
            email_verified=True,
            auth0_name="Test User",
            display_name="Test Display Name",
            role="Student"
        )

        #Create an instructor user for course
        self.instructor = User.objects.create(
            auth_id="987654321",
            email="instructor@example.com",
            email_verified=True,
            auth0_name="Instructor User",
            display_name="Instructor Display Name",
            role="Instructor"
        )

        # Create a course
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            status="Current",
            instructor=self.instructor
        )

    def test_create_enrollment(self):
        url = '/createenrollment/'
        data = {
            "user_id": self.student.id,
            "course_id": self.course.id,
            "grade": 70.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_get_enrollments_for_user(self):
        # Create an enrollment for the student
        url = '/createenrollment/'
        data = {
            "user_id": self.student.id,
            "course_id": self.course.id,
            "grade": 95.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = f'/enrollments/{self.student.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.course.name)
        self.assertEqual(response.data[0]['instructor']['id'], self.instructor.id)
        self.assertEqual(response.data[0]['grade'], 95.00)

    def test_invalid_enrollment(self):
        url = '/createenrollment/'

        # Create an enrollment with an invalid user ID
        data = {
            "user_id": "654",
            "course_id": self.course.id,
            "grade": 50.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create an enrollment with an invalid course ID
        data = {
            "user_id": self.student.id,
            "course_id": "1111",
            "grade": 100.00
        }
        response = self.client.post(url, data, format='json')
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