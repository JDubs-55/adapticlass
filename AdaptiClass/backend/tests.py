import json, uuid, dateutil.parser
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


## ASSIGNMENT TEST CASES
class AssignmentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a course
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            status="Current",
            instructor=User.objects.create(
                auth_id="123456789",
                email="instructor@example.com",
                email_verified=True,
                auth0_name="Instructor User",
                display_name="Instructor Display Name",
                role="Instructor"
            )
        )

        # Create a student
        self.student = User.objects.create(
            auth_id="987654321",
            email="student@example.com",
            email_verified=True,
            auth0_name="Student User",
            display_name="Student Display Name",
            role="Student"
        )

    def test_create_assignment(self):
        url = f'/assignments/{self.course.id}/'
        data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 1)

    def test_get_assignment_list(self):
        # Create an assignment
        url = f'/assignments/{self.course.id}/'
        ass_data1 = {
            "course": self.course.id,
            "title": "Test Assignment 1",
            "description": "Test Description 1",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create another assignment
        url = f'/assignments/{self.course.id}/'
        ass_data2 = {
            "course": self.course.id,
            "title": "Test Assignment 2",
            "description": "Test Description 2",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_assignment_detail(self):
        # Create an assignment
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        assignment = Assignment.objects.get(id = response.data['id'])
        url = f'/assignment/{assignment.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course'], self.course.id)
        self.assertEqual(response.data['title'], "Test Assignment")
        self.assertEqual(response.data['description'], "Test Description")
        self.assertEqual(response.data['status'], "Upcoming")
        self.assertEqual(response.data['due_date'], "2024-04-20")
        self.assertEqual(response.data['created_by'], self.course.instructor.id)


    def test_modify_assignment(self):
        # Create an assignment
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

         # Modify the assignment
        assignment = Assignment.objects.get(id = response.data['id'])
        url = f'/assignment/{assignment.id}/'
        modified_data = {
            "course": self.course.id,
            "title": "Modified Assignment",
            "description": "Modified Description",
            "status": "Upcoming",
            "due_date": "2024-05-01",
            "created_by": self.course.instructor.id
        }
        response = self.client.put(url, modified_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Check if the assignment details have been updated
        modified_assignment = Assignment.objects.get(id=assignment.id)
        self.assertEqual(modified_assignment.title, "Modified Assignment")
        self.assertEqual(modified_assignment.description, "Modified Description")
        self.assertEqual(str(modified_assignment.due_date), "2024-05-01")

    def test_invalid_assignment(self):
        # Invalid course ID (note the plural 'assignments')
        url = '/assignments/9999/' 
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid assignment ID
        url = '/assignment/9999/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Create assignment with no course data
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create assignment with improper status
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Wrong Status",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create assignment with no created_by
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20"
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create assignment with no due date
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create an assignment with no title
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_student_assignment_list(self):
        # Create an assignment
        url = f'/assignments/{self.course.id}/'
        ass_data1 = {
            "course": self.course.id,
            "title": "Test Assignment 1",
            "description": "Test Description 1",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response1 = self.client.post(url, ass_data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Create another assignment
        ass_data2 = {
            "course": self.course.id,
            "title": "Test Assignment 2",
            "description": "Test Description 2",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response2 = self.client.post(url, ass_data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Associate the assignments with the student
        assignment1 = Assignment.objects.get(id = response1.data['id'])
        assignment2 = Assignment.objects.get(id = response2.data['id'])
        UserAssignment.objects.create(
            user=self.student,
            assignment=assignment1,
            grade = 95.00,
            is_complete = True
        )

        UserAssignment.objects.create(
            user=self.student,
            assignment=assignment2,
            grade = 50.00,
            is_complete = False
        )

        url = f'/student/assignments/{self.course.id}/?user_id={self.student.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check assignment 1 data
        self.assertEqual(response.data[0]['course'], self.course.id)
        self.assertEqual(response.data[0]['title'], "Test Assignment 1")
        self.assertEqual(response.data[0]['description'], "Test Description 1")
        self.assertEqual(response.data[0]['status'], "Upcoming")
        self.assertEqual(response.data[0]['due_date'], "2024-04-20")
        self.assertEqual(response.data[0]['created_by'], self.course.instructor.id)
        self.assertEqual(response.data[0]['grade'], 95.00)
        self.assertTrue(response.data[0]['is_complete'])

        # Check assignment 2 data
        self.assertEqual(response.data[1]['course'], self.course.id)
        self.assertEqual(response.data[1]['title'], "Test Assignment 2")
        self.assertEqual(response.data[1]['description'], "Test Description 2")
        self.assertEqual(response.data[1]['status'], "Upcoming")
        self.assertEqual(response.data[1]['due_date'], "2024-04-20")
        self.assertEqual(response.data[1]['created_by'], self.course.instructor.id)
        self.assertEqual(response.data[1]['grade'], 50.00)
        self.assertFalse(response.data[1]['is_complete'])

    def test_get_student_assignment_detail(self):
        # Create an assignment
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Associate the assignment with the student
        assignment = Assignment.objects.get(id = response.data['id'])
        UserAssignment.objects.create(
            user=self.student,
            assignment=assignment,
            grade = 75.00,
            is_complete = False
        )

        url = f'/student/assignment/{assignment.id}/?user_id={self.student.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course'], self.course.id)
        self.assertEqual(response.data['title'], "Test Assignment")
        self.assertEqual(response.data['description'], "Test Description")
        self.assertEqual(response.data['status'], "Upcoming")
        self.assertEqual(response.data['due_date'], "2024-04-20")
        self.assertEqual(response.data['created_by'], self.course.instructor.id)
        self.assertEqual(response.data['grade'], 75.00)
        self.assertFalse(response.data['is_complete'])

    def test_no_assignments_for_student(self):
        # Create an assignment without associating it with the student
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch student assignments without associating the assignment with the student
        url = f'/student/assignments/{self.course.id}/?user_id={self.student.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_student_id(self):
        # Create an assignment
        url = f'/assignments/{self.course.id}/'
        ass_data = {
            "course": self.course.id,
            "title": "Test Assignment",
            "description": "Test Description",
            "status": "Upcoming",
            "due_date": "2024-04-20",
            "created_by": self.course.instructor.id
        }
        response = self.client.post(url, ass_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = f'/student/assignments/{self.course.id}/?user_id=9999'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


## ACTIVITY TEST CASES
class ActivityTestCase(TestCase):
    def setUp(self):
        # Create an instructor user
        self.instructor = User.objects.create(
            auth_id="987654321",
            email="instructor@example.com",
            email_verified=True,
            auth0_name="Instructor User",
            display_name="Instructor Display Name",
            role="Instructor"
        )

        # Create a student user
        self.student = User.objects.create(
            auth_id="123456789",
            email="student@example.com",
            email_verified=True,
            auth0_name="Student User",
            display_name="Student Display Name",
            role="Student"
        )

        # Create a course
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            status="Current",
            instructor=self.instructor
        )

        # Create an assignment
        self.assignment = Assignment.objects.create(
            course=self.course,
            title="Test Assignment",
            description="Test Description",
            status="Upcoming",
            due_date="2024-04-20",
            created_by=self.instructor
        )


    def test_create_activity(self):
        # Create a new activity
        url = f'/activities/{self.assignment.id}/'
        act_data = {
            'assignment': self.assignment.id,
            'title': "New Activity",
            'type': "Assessment"
        }
        response = self.client.post(url, act_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)


    def test_modify_activity(self):
        # Create an activity
        url = f'/activities/{self.assignment.id}/'
        act_data = {
            'assignment': self.assignment.id,
            'title': "New Activity",
            'type': "Assessment"
        }
        response = self.client.post(url, act_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Modify the activity
        activity = Activity.objects.get(assignment=self.assignment)
        url = f'/activity/{activity.id}/'
        data = {
            "assignment": self.assignment.id,
            "title": "Updated Activity",
            "type": "Exercise"
        }
        json_data = json.dumps(data)
        response = self.client.put(url, json_data, content_type='application/json')


        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        updated_activity = Activity.objects.get(pk=activity.id)
        self.assertEqual(updated_activity.assignment, self.assignment)
        self.assertEqual(updated_activity.title, "Updated Activity")
        self.assertEqual(updated_activity.type, "Exercise")

    def test_delete_activity(self):
        # Create an activity
        url = f'/activities/{self.assignment.id}/'
        act_data = {
            'assignment': self.assignment.id,
            'title': "New Activity",
            'type': "Assessment"
        }
        response = self.client.post(url, act_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        activity = Activity.objects.get(assignment=self.assignment)
        url = f'/activity/{activity.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Activity.objects.count(), 0)

    def test_invalid_activity_requests(self):
        # List activities with an invalid assignment ID (should be empty list)
        url = f'/activities/999/'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

        # Get details of activity that doesnt exist
        url = '/activity/999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Create acitivty with no assignment
        url = f'/activities/{self.assignment.id}/'
        act_data = {
            'title': "New Activity",
            'type': "Assessment"
        }
        response = self.client.post(url, act_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create activity with no title
        url = f'/activities/{self.assignment.id}/'
        act_data = {
            'assignment': self.assignment.id,
            'type': "Assessment"
        }
        response = self.client.post(url, act_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        # Create activity with invlaid type
        url = f'/activities/{self.assignment.id}/'
        act_data = {
            'assignment': self.assignment.id,
            'title': "New Activity",
            'type': "Wrong Type"
        }
        response = self.client.post(url, act_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

## QUESTION TEST CASES
class QuestionTestCase(APITestCase):
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

        # Create a user to use as an instructor
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
            instructor=self.instructor,
            course_image="https://example.com/course.jpg"
        )

        # Create an assignment
        self.assignment = Assignment.objects.create(
            course=self.course,
            title="Test Assignment",
            description="Test Description",
            status="Upcoming",
            due_date="2024-04-20",
            created_by=self.instructor
        )

        # Create an activity
        self.activity = Activity.objects.create(
            assignment=self.assignment,
            title="Test Activity",
            type="Exercise" 
            )

    def test_create_question(self):
        url = f'/questions/{self.activity.id}/'
        question_data = {
            'activity': self.activity.id,
            'question': 'What is 2 + 2?',
            'answer': str(2 + 2)
        }
        response = self.client.post(url, question_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)


    def test_get_question_list(self):
        url = f'/questions/{self.activity.id}/'
        question_data1 = {
            'activity': self.activity.id,
            'question': 'What is 2 + 2?',
            'answer': str(2+2)
        }
        response = self.client.post(url, question_data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        question_data2 = {
            'activity': self.activity.id,
            'question': 'What is 57 * 32?',
            'answer': str(57 * 32)
        }
        response = self.client.post(url, question_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Question.objects.count(), 2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["question"], 'What is 2 + 2?')
        self.assertEqual(response.data[0]["answer"], str(2+2))
        self.assertEqual(response.data[1]["question"], 'What is 57 * 32?')
        self.assertEqual(response.data[1]["answer"], str(57 * 32))


    def test_get_question_detail(self):
        url = f'/questions/{self.activity.id}/'
        question_data = {
            'activity': self.activity.id,
            'question': 'What is 2 + 2?',
            'answer': str(2+2)
        }
        response = self.client.post(url, question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        question = Question.objects.get(activity=self.activity)
        url = f'/question/{question.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["activity"], self.activity.id)
        self.assertEqual(response.data["question"], 'What is 2 + 2?')
        self.assertEqual(response.data["answer"], str(2+2))

    def test_update_question(self):
        url = f'/questions/{self.activity.id}/'
        question_data = {
            'activity': self.activity.id,
            'question': 'What is 2 + 2?',
            'answer': str(2+2)
        }
        response = self.client.post(url, question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        updated_data = {
            'activity': self.activity.id,
            'question': 'What is 3 + 3?',
            'answer': str(3 + 3)
        }
        
        question = Question.objects.get(activity=self.activity)
        url = f'/question/{question.id}/'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["question"], 'What is 3 + 3?')
        self.assertEqual(response.data["answer"], str(3 + 3))

    def test_delete_question(self):
        url = f'/questions/{self.activity.id}/'
        question_data = {
            'activity': self.activity.id,
            'question': 'What is 2 + 2?',
            'answer': str(2+2)
        }
        response = self.client.post(url, question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        question = Question.objects.get(activity=self.activity)
        url = f'/question/{question.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

    def test_invalid_question_requests(self):
        # Create a question without an activity
        url = f'/questions/{self.activity.id}/'
        invalid_question_data = {
            'question': 'What is 2 + 2?',
            'answer': str(2 + 2)
        }
        response = self.client.post(url, invalid_question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create a question without a question
        url = f'/questions/{self.activity.id}/'
        invalid_question_data = {
            'activity': self.activity.id,
            'answer': str(2 + 2)
        }
        response = self.client.post(url, invalid_question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create a question without an answer
        url = f'/questions/{self.activity.id}/'
        invalid_question_data = {
            'activity': self.activity.id,
            'question': 'What is 2 + 2?',
        }
        response = self.client.post(url, invalid_question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Getting a question that does not exist
        url = f'/question/9999/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Updating a question that does not exist
        url = f'/question/9999/'
        updated_data = {
            'activity': self.activity.id,
            'question': 'What is 3 + 3?',
            'answer': str(3 + 3)
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Deleting a question that does not exist
        url = f'/question/9999/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_associate_question_with_user(self):
        url = f'/questions/{self.activity.id}/'
        question_data = {
            'activity': self.activity.id,
            'question': 'What is 2 + 2?',
            'answer': str(2 + 2)
        }
        response = self.client.post(url, question_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure UserQuestion is associated with the correct user and question
        question = Question.objects.get(activity=self.activity)
        user_question = UserQuestion.objects.create(
            user=self.student,
            question=question,
            is_answered=False,
            is_correct=False,
            user_answer=''
        )
        # Retrieve the associated question and check its attributes
        self.assertEqual(user_question.user, self.student)
        self.assertEqual(user_question.question.activity.id, question_data['activity'])
        self.assertEqual(user_question.question.question, question_data['question'])
        self.assertEqual(user_question.question.answer, question_data['answer'])

        # Update the user question with an incorrect user answer
        user_answer = str(5 + 2)
        user_question.user_answer = user_answer
        is_correct = (user_answer == question_data['answer'])
        is_answered = (user_answer != '')
        user_question.is_answered = is_answered
        user_question.is_correct = is_correct
        user_question.save()

        self.assertTrue(user_question.is_answered)
        self.assertFalse(user_question.is_correct)

        # Update the user question with a correct user answer
        user_answer = str(2 + 2)
        user_question.user_answer = user_answer
        is_correct = (user_answer == question_data['answer'])
        is_answered = (user_answer != '')
        user_question.is_answered = is_answered
        user_question.is_correct = is_correct
        user_question.save()

        self.assertTrue(user_question.is_answered)
        self.assertTrue(user_question.is_correct)


## ENGAGEMENT TEST CASES
class EngagementTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.student = User.objects.create(
            auth_id="123456789",
            email="test@example.com",
            email_verified=True,
            auth0_name="Test User",
            display_name="Test Display Name",
            role="Student"
        )

        # Create a user to use as an instructor
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
            instructor=self.instructor,
            course_image="https://example.com/course.jpg"
        )

        self.assignment = Assignment.objects.create(
            course=self.course,
            title="Test Assignment",
            description="Test Description",
            status="Upcoming",
            due_date="2024-04-20",
            created_by=self.instructor
        )

        self.url = '/engagementdata/'

    def test_create_engagement_data(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'assignment': self.assignment.id,
            'start': start_time,
            'end': end_time,
            'total_time': end_time - start_time,
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_retrieve_engagement_data(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'assignment': self.assignment.id,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'total_time': (end_time - start_time).total_seconds(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url)

        # Convert strings to datetime objects for comparison
        start_time_response = dateutil.parser.parse(response.data[0]["start"])
        end_time_response = dateutil.parser.parse(response.data[0]["end"])
        start_time_data = dateutil.parser.parse(data["start"])
        end_time_data = dateutil.parser.parse(data["end"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["user"], self.student.id)
        self.assertEqual(response.data[0]["assignment"], self.assignment.id)
        self.assertEqual(start_time_response, start_time_data)
        self.assertEqual(end_time_response, end_time_data)
        self.assertEqual(response.data[0]["total_time"], 3600)
        self.assertEqual(response.data[0]["engaged_time"], 1800)

    def test_create_engagement_period(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'assignment': self.assignment.id,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'total_time': (end_time - start_time).total_seconds(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        engagement_data = EngagementData.objects.get(user=self.student.id, start=start_time)
        
        # Create engagement period data
        start_timestamp = timezone.now().timestamp()
        end_timestamp = (timezone.now() + timezone.timedelta(hours=1)).timestamp()
        period_data = {
            'engagement_data': engagement_data,
            'state': "Active",
            'start': start_timestamp,
            'duration': 3600,
            'end': end_timestamp
        }

        # Create the engagement period
        engagement_period = EngagementPeriod.objects.create(**period_data)

        # Assert that the engagement period was created successfully
        self.assertEqual(engagement_period.state, "Active")
        self.assertEqual(engagement_period.start, start_timestamp)
        self.assertEqual(engagement_period.duration, 3600)
        self.assertEqual(engagement_period.end, end_timestamp)

    def test_retrieve_engagement_period(self):
        # Create engagement data
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'assignment': self.assignment.id,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'total_time': (end_time - start_time).total_seconds(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        engagement_data = EngagementData.objects.get(user=self.student.id, start=start_time)

        # Create engagement period
        period_start = start_time.timestamp()  # Convert to Unix timestamp
        period_end = (start_time + timezone.timedelta(hours=1)).timestamp()  # Convert to Unix timestamp
        engagement_period = EngagementPeriod.objects.create(
            engagement_data=engagement_data,
            state="Active",
            start=period_start,
            duration=3600,
            end=period_end
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Check that engagement data is correct
        retrieved_engagement_data = response.data[0]

        # Convert strings to datetime objects for comparison
        start_time_response = dateutil.parser.parse(retrieved_engagement_data["start"])
        end_time_response = dateutil.parser.parse(retrieved_engagement_data["end"])
        start_time_data = dateutil.parser.parse(data["start"])
        end_time_data = dateutil.parser.parse(data["end"])

        self.assertEqual(retrieved_engagement_data['user'], self.student.id)
        self.assertEqual(retrieved_engagement_data['assignment'], self.assignment.id)
        self.assertEqual(start_time_response, start_time_data)
        self.assertEqual(end_time_response, end_time_data)
        self.assertEqual(retrieved_engagement_data['total_time'], (end_time - start_time).total_seconds())
        self.assertEqual(retrieved_engagement_data['engaged_time'], 1800)

        # Assert the correctness of retrieved engagement period
        retrieved_period = response.data[0]['engagement_periods'][0]  # Adjusted to access nested engagement data
        self.assertEqual(retrieved_period['engagement_data'], engagement_period.engagement_data.id)
        self.assertEqual(retrieved_period['state'], engagement_period.state)
        self.assertEqual(retrieved_period['start'], engagement_period.start)
        self.assertEqual(retrieved_period['duration'], engagement_period.duration)
        self.assertEqual(retrieved_period['end'], engagement_period.end)

    def test_invalid_input(self):
        # Try to create engagement data with no user
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'assignment': self.assignment.id,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'total_time': (end_time - start_time).total_seconds(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to create engagement data with no assignment
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'total_time': (end_time - start_time).total_seconds(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to create engagement data with no start time
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'assignment': self.assignment.id,
            'end': end_time.isoformat(),
            'total_time': (end_time - start_time).total_seconds(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to create engagement data with no end time
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'assignment': self.assignment.id,
            'start': start_time.isoformat(),
            'total_time': (end_time - start_time).total_seconds(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to create engagement data without total time
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        data = {
            'user': self.student.id,
            'assignment': self.assignment.id,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'engaged_time': 1800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

## CHAT TEST CASES
class ChatTestCase(APITestCase):
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

        # Create a user to use as an instructor
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
            instructor=self.instructor,
            course_image="https://example.com/course.jpg"
        )

        # Create an assignment
        self.assignment = Assignment.objects.create(
            course=self.course,
            title="Test Assignment",
            description="Test Description",
            status="Upcoming",
            due_date="2024-04-20",
            created_by=self.instructor
        )

        # Create a chat record
        self.chat = Chat.objects.create(
            auth_id=self.student,
            assignment_id=self.assignment,
            question="Explain how to solve 2x + 3 = 11.",
            solution=""
        )

    def test_chat_response(self):
        """
        Ensure that the chatbot returns a response.
        """
        url = reverse('chatbot_view')
        data = {'question': self.chat.question}
        response = self.client.post(url, data, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "API should not return 400 Bad Request")
        self.assertIn('solution', response.data, "Response data should contain a 'solution' key")

    def test_chat_no_question(self):
        """
        Ensure that the chatbot returns an error when no question is provided.
        """
        url = reverse('chatbot_view')
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Question is required.')

    def test_save_and_retrieve_chat_record(self):
        """
        Ensure that chat records are saved correctly and can be retrieved using auth_id and assignment_id.
        """
        retrieved_chat = Chat.objects.get(auth_id=self.student, assignment_id=self.assignment)
        self.assertIsNotNone(retrieved_chat, "Chat record should be retrievable.")
        self.assertEqual(retrieved_chat.question, "Explain how to solve 2x + 3 = 11.", "The question should match the one saved.")
        self.assertEqual(retrieved_chat.solution, "", "Initially, the solution should be empty.")

    def test_updating_chat_record(self):
        """
        Test updating a chat record to simulate storing a solution after chatbot processing.
        """
        retrieved_chat = Chat.objects.get(auth_id=self.student, assignment_id=self.assignment)
        retrieved_chat.solution = "To solve 2x + 3 = 11, first subtract 3 from both sides to get 2x = 8, then divide both sides by 2 to get x = 4."
        retrieved_chat.save()

        updated_chat = Chat.objects.get(auth_id=self.student, assignment_id=self.assignment)
        self.assertEqual(updated_chat.solution, "To solve 2x + 3 = 11, first subtract 3 from both sides to get 2x = 8, then divide both sides by 2 to get x = 4.", "The solution should be updated correctly.")

    def test_retrieval_by_incorrect_parameters(self):
        """
        Ensure that querying with incorrect parameters does not retrieve any records.
        """
        with self.assertRaises(Chat.DoesNotExist):
            Chat.objects.get(auth_id=self.student, assignment_id=99999)

    def test_multiple_chats_same_assignment(self):
        """
        Test that multiple chats can be created for the same assignment and retrieved correctly.
        """
        # Create another chat for the same assignment but different student
        another_student = User.objects.create(
            auth_id="123123123",
            email="another@example.com",
            email_verified=True,
            auth0_name="Another User",
            display_name="Another Display Name",
            role="Student"
        )
        Chat.objects.create(
            auth_id=another_student,
            assignment_id=self.assignment,
            question="Explain how to solve 3x - 2 = 4.",
            solution=""
        )

        chats = Chat.objects.filter(assignment_id=self.assignment).count()
        self.assertEqual(chats, 2, "There should be two chats for the same assignment.")

    def test_multiple_chats_same_student_same_assignment(self):
        """
        Test that multiple chats can be created for the same student and the same assignment and retrieved correctly.
        """
        # Create additional chats for the same student and assignment with different questions
        Chat.objects.create(
            auth_id=self.student,
            assignment_id=self.assignment,
            question="Explain how to solve x^2 + 5x + 6 = 0.",
            solution=""
        )
        Chat.objects.create(
            auth_id=self.student,
            assignment_id=self.assignment,
            question="Describe the process to graph the equation y = 2x + 3.",
            solution=""
        )

        # Retrieve all chats for this student and assignment to confirm they are saved and retrieved correctly
        chats = Chat.objects.filter(auth_id=self.student, assignment_id=self.assignment)
        self.assertEqual(chats.count(), 3, "There should be three chat records for the same student and the same assignment.")

        # Check details of the chats to ensure data integrity
        questions = {chat.question for chat in chats}
        expected_questions = {
            "Explain how to solve 2x + 3 = 11.",
            "Explain how to solve x^2 + 5x + 6 = 0.",
            "Describe the process to graph the equation y = 2x + 3."
        }
        self.assertEqual(questions, expected_questions, "The questions in the chats should match the expected set.")

    def test_multiple_chats_one_student_different_assignments(self):
        """
        Test that a student can have multiple chats across different assignments and that these can be retrieved correctly.
        """
        # Create another assignment
        another_assignment = Assignment.objects.create(
            course=self.course,
            title="Another Test Assignment",
            description="Another Test Description",
            status="Upcoming",
            due_date="2024-05-15",
            created_by=self.instructor
        )

        # Create chats for the different assignments
        Chat.objects.create(
            auth_id=self.student,
            assignment_id=self.assignment,  # First assignment
            question="Explain how to solve 2x + 3 = 11.",
            solution=""
        )
        Chat.objects.create(
            auth_id=self.student,
            assignment_id=another_assignment,  # Second assignment
            question="Describe the process to graph the equation y = 2x + 3.",
            solution=""
        )

        # Retrieve all chats for this student to confirm correct creation across assignments
        chats = Chat.objects.filter(auth_id=self.student)
        self.assertEqual(chats.count(), 3, "There should be three chat records for the student across different assignments.")

        # Verify that the chats belong to the correct assignments
        chat_assignments = {chat.assignment_id for chat in chats}
        expected_assignments = {self.assignment, another_assignment}
        self.assertEqual(chat_assignments, expected_assignments, "The chats should be linked to the expected assignments.")

        # Check the questions to ensure data integrity
        questions = {chat.question for chat in chats}
        expected_questions = {
            "Explain how to solve 2x + 3 = 11.",
            "Explain how to solve 2x + 3 = 11.",
            "Describe the process to graph the equation y = 2x + 3."
        }
        self.assertEqual(questions, expected_questions, "The questions in the chats should match the expected set.")

class AlternativeQuestionGenerationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Set up user, course, assignment, and activity as before
        self.student = User.objects.create(
            auth_id="123456789",
            email="test@example.com",
            email_verified=True,
            auth0_name="Test User",
            display_name="Test Display Name",
            role="Student"
        )
        self.instructor = User.objects.create(
            auth_id="987654321",
            email="instructor@example.com",
            email_verified=True,
            auth0_name="Instructor User",
            display_name="Instructor Display Name",
            role="Instructor"
        )
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            status="Current",
            instructor=self.instructor,
            course_image="https://example.com/course.jpg"
        )
        self.assignment = Assignment.objects.create(
            course=self.course,
            title="Test Assignment",
            description="Test Description",
            status="Upcoming",
            due_date="2024-04-20",
            created_by=self.instructor
        )
        self.activity = Activity.objects.create(
            assignment=self.assignment,
            title="Test Activity",
            type="Exercise"
        )

    def test_successful_question_generation(self):
        """
        Ensure that the ProblemGeneratorView generates a question and answer, and they are saved correctly.
        """
        url = reverse('generator_view')
        sample_question = "Explain how to solve 2x + 3 = 11."
        data = {'question': sample_question}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('question', response.data)
        self.assertIn('answer', response.data)

        # Attempt to save the generated question and answer
        question_text = response.data['question']
        answer_text = response.data['answer']
        new_question = Question.objects.create(
            activity=self.activity,
            question=question_text,
            answer=answer_text
        )

        # Verify the saved data
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(new_question.question, question_text)
        self.assertEqual(new_question.answer, answer_text)

    def test_invalid_question_generation(self):
        """
        Ensure that the view handles non-Algebra 1 related questions appropriately.
        """
        url = reverse('generator_view')
        invalid_question = "What is the capital of France?"
        data = {'question': invalid_question}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'The provided problem is not related to Algebra 1.')

