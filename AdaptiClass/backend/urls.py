from django.urls import path
from . views import *

urlpatterns = [
    path('courses/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail_view'),
    path('courses/<int:pk>/removeusers/', RemoveUsersFromCourseView.as_view()),
    path('users/', UserListView.as_view()), #Retrieve List of user or post new user
    path('users/<str:user_id>/', UserDetailView.as_view()), #Retrieve user info by id, 200 success/404 not_found
    # path('courses/<int:course_id>/sections/<int:section_id>/', SectionDetailView.as_view()),
    # path('courses/<int:course_id>/sections/<int:section_id>/assignments/<int:assignment_id>/', AssignmentDetailView.as_view()),
    # path('courses/<str:course_name>/sections/', SectionListView.as_view()),  # Endpoint for creating sections under a course
    # path('courses/<str:course_name>/sections/<int:section_id>/assignments/', AssignmentListView.as_view()),  # Endpoint for creating assignments under a section
    path('chat/', ChatbotView.as_view(), name='chatbot_view'),
]

