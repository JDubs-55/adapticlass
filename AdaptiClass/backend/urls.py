from django.urls import path
from . views import *

urlpatterns = [
    
    path('users/', UserListView.as_view()), #Retrieve List of user or post new user
    path('users/<str:auth_id>/', UserDetailView.as_view()), #Retrieve user info by id, 200 success/404 not_found
    
    path('courses/', CourseListView.as_view()),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='course_detail_view'),

    path('enrollments/<str:user_id>/', CourseEnrollmentListView.as_view()),
    path('createenrollment/', CreateEnrollment.as_view()),

    #Primarily for teacher, student will see assignments with their info. 
    path('assignments/', TestAssignmentListView.as_view()),
    path('assignments/<int:course_id>/', AssignmentListView.as_view()),
    path('assignment/<int:assignment_id>/', AssignmentDetailView.as_view()),
    path('student/assignments/<int:course_id>/', UserAssignmentListView.as_view()),
    path('student/assignment/<int:assignment_id>/', UserAssignmentDetailView.as_view()),
    path('assignmentcompleted/', UserAssignmentSetComplete.as_view()),
    
    path('activities/', TestActivityListView.as_view()),
    path('activities/<int:assignment_id>/', ActivityListView.as_view()),
    path('activity/<int:activity_id>/', ActivityDetailView.as_view()),
    path('activitycompleted/', UserActivitySetComplete.as_view()),
    
    path('questions/', TestQuestionListView.as_view()),
    path('questions/<int:activity_id>/', QuestionListView.as_view()),
    path('question/<int:question_id>/', QuestionDetailView.as_view()),
    path('userquestions/<int:activity_id>/', UserQuestionListView.as_view()),
    

    ##path('courses/<int:pk>/removeusers/', RemoveUsersFromCourseView.as_view()), NOT Needed if we are using enrollments
    ##path('coursegrade/<str:course_name>/', CourseGradeView.as_view()), NOT Needed, attach grade to enrollment. 
    ##path('enrollments/', UserEnrollmentView.as_view()), # Moved/Refactored
    ##path('assignments/', AssignmentListView.as_view()), # Refactored view. 
    ##path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail_view'),  # To retrieve, update, or delete an assignment
    ##path('assignments/<str:course_name>/', CourseAssignmentListView.as_view(), name='course_assignment_view'), ##Refactored and changed to search by id. 
    # path('assignmentgrade/<str:course_name>/', AssignmentGradesByCourseView.as_view()),
    # path('assignmentgrade/<str:course_name>/<int:assignment_id>/', AssignmentGradeView.as_view()),
    # path('assignmentquestions/', AssignmentQuestionListView.as_view()),
    # path('assignmentquestions/<int:assignment_id>/', AssignmentQuestionByIDView.as_view()),
    # path('assignmentquestions/<int:assignment_id>/<int:question_id>/', AssignmentQuestionDetailView.as_view(), name = 'assignmentquestion_detail_view'),

    # #I think alternate questions should just be a question with a flag. 
    # path('alternatequestions/', AlternateQuestionListView.as_view()),
    # path('alternatequestions/<int:pk>/', AlternateQuestionDetailView.as_view(), name = 'alternatequestion_detail_view'),


    # path('questions/', QuestionListView.as_view()),
    # path('questions/<int:pk>/', QuestionDetailView.as_view(), name = 'question_detail_view'),


    path('chat/', ChatbotView.as_view(), name='chatbot_view'),
    path('problemgenerator/', ProblemGeneratorView.as_view(), name='generator_view'),
    
    path('engagementdata/', EngagementDataAPIView.as_view(), name='engagementdata_list_view')
]

