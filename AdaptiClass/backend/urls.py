from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student_list_view'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail_view'),
    path('instructors/', InstructorListView.as_view(), name='instructor_list_view'),
    path('instructors/<int:pk>/', InstructorDetailView.as_view(), name='instructor_detail_view'),
    path('courses/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail_view'),
    path('courses/<int:pk>/removestudents/', RemoveStudentsFromCourseView.as_view()),
    path('users/', UserListView.as_view()),  # Retrieve List of user or post new user
    path('users/<str:user_id>/', UserDetailView.as_view()),  # Retrieve user info by id, 200 success/404 not_found
    path('courses/<int:course_id>/sections/<int:section_id>/', SectionDetailView.as_view()),
    path('courses/<int:course_id>/sections/<int:section_id>/assignments/<int:assignment_id>/',
         AssignmentDetailView.as_view()),
    path('courses/<str:course_name>/sections/', SectionListView.as_view()),
    # Endpoint for creating sections under a course
    path('courses/<int:section_id>/assignments/', AssignmentListView.as_view()),
    # Endpoint for creating assignments under a section
    path('chat/', ChatbotView.as_view(), name='chatbot_view'),
]
