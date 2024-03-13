from django.urls import path
from . views import *

urlpatterns = [
    path('students/', StudentListView.as_view()),
    path('students/<str:email>/', StudentDetailView.as_view()),
    path('instructors/', InstructorListView.as_view()),
    path('instructors/<str:email>/', InstructorDetailView.as_view()),
    path('courses/', CourseListView.as_view()),
    path('courses/<str:name>/', CourseDetailView.as_view()),
    # path('courses/<str:name>/addstudent/', AddStudentToCourseView.as_view()),
    path('courses/<str:name>/removestudents/', RemoveStudentsFromCourseView.as_view()),


<<<<<<< HEAD
    path('courses/<int:course_id>/sections/<int:section_id>/', SectionDetailView.as_view()),
    path('courses/<int:course_id>/sections/<int:section_id>/assignments/<int:assignment_id>/', AssignmentDetailView.as_view()),
=======
    path('courses/<str:course_name>/sections/', SectionListView.as_view()),  # Endpoint for creating sections under a course
    path('courses/<str:course_name>/sections/<int:section_id>/assignments/', AssignmentListView.as_view()),  # Endpoint for creating assignments under a section
>>>>>>> 3e1113e471d135658744227d16ee80c623ee7f0a
]

