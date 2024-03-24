from django.urls import path
from . views import *

urlpatterns = [
    path('courses/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail_view'),
    path('courses/<int:pk>/removeusers/', RemoveUsersFromCourseView.as_view()),
    path('users/', UserListView.as_view()), #Retrieve List of user or post new user
    path('users/<str:user_id>/', UserDetailView.as_view()), #Retrieve user info by id, 200 success/404 not_found
    path('sections/<int:pk>/', SectionDetailView.as_view(), name='section_detail_view'),  # To retrieve, update, or delete a section
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail_view'),  # To retrieve, update, or delete an assignment

    # To list or create sections under a specific course
    path('courses/<int:course_id>/sections/', SectionListView.as_view(), name='course_sections_list_view'),
    # To list or create assignments under a specific section
    path('sections/<int:section_id>/assignments/', AssignmentListView.as_view(), name='section_assignments_list_view'),
    path('chat/', ChatbotView.as_view(), name='chatbot_view'),
]

