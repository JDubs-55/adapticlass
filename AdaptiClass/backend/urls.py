from django.urls import path
from . views import *

urlpatterns = [
    path('students/', StudentListView.as_view()),
    path('students/<int:id>/', StudentDetailView.as_view()),
    # path('students/<str:email>/', StudentDetailView.as_view()),
    path('instructors/', InstructorListView.as_view()),
    path('instructors/<str:email>/', InstructorDetailView.as_view()),
    path('courses/', CourseListView.as_view()),
    path('courses/<str:name>/', CourseDetailView.as_view()),
    # path('courses/<str:name>/addstudent/', AddStudentToCourseView.as_view()),
    path('courses/<str:name>/removestudents/', RemoveStudentsFromCourseView.as_view()),
]
