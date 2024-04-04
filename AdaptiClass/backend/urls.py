from django.urls import path
from . views import *

urlpatterns = [
    
    path('users/', UserListView.as_view()), #Retrieve List of user or post new user
    path('users/<str:user_id>/', UserDetailView.as_view()), #Retrieve user info by id, 200 success/404 not_found
    path('enrollments/<str:user_id>/', CourseEnrollmentListView.as_view()),
    path('createenrollment/', CreateEnrollment.as_view()),
    
    path('courses/', CourseListView.as_view()),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail_view'),
    path('courses/<int:pk>/removeusers/', RemoveUsersFromCourseView.as_view()),
    path('coursegrade/<str:course_name>/', CourseGradeView.as_view()),
    
    path('enrollments/', UserEnrollmentView.as_view()),
    path('assignments/', AssignmentListView.as_view()),
    
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail_view'),  # To retrieve, update, or delete an assignment
    path('assignments/<str:course_name>/', CourseAssignmentListView.as_view(), name='course_assignment_view'),
    path('assignmentgrade/<str:course_name>/', AssignmentGradesByCourseView.as_view()),
    path('assignmentgrade/<str:course_name>/<int:assignment_id>/', AssignmentGradeView.as_view()),
    path('assignmentquestions/', AssignmentQuestionListView.as_view()),
    path('assignmentquestions/<int:assignment_id>/', AssignmentQuestionByIDView.as_view()),
    path('assignmentquestions/<int:assignment_id>/<int:question_id>/', AssignmentQuestionDetailView.as_view(), name = 'assignmentquestion_detail_view'),

    path('alternatequestions/', AlternateQuestionListView.as_view()),
    path('alternatequestions/<int:pk>/', AlternateQuestionDetailView.as_view(), name = 'alternatequestion_detail_view'),


    path('questions/', QuestionListView.as_view()),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name = 'question_detail_view'),


    path('chat/', ChatbotView.as_view(), name='chatbot_view'),
    path('problemgenerator/', ProblemGeneratorView.as_view(), name='generator_view'),
    
    path('engagementdata/', EngagementDataAPIView.as_view(), name='engagementdata_list_view')
]

