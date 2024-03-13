from django.urls import path
from . views import *

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student_list_view'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail_view'),
    path('instructors/', InstructorListView.as_view(), name='instructor_list_view'),
    path('instructors/<int:pk>/', InstructorDetailView.as_view(), name='instructor_detail_view'),
    path('courses/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail_view'),
    path('courses/<int:pk>/removestudents/', RemoveStudentsFromCourseView.as_view()),
    path('users/', UserListView.as_view()), #Retrieve List of user or post new user
    path('users/<str:user_id>/', UserDetailView.as_view()), #Retrieve user info by id, 200 success/404 not_found
]
