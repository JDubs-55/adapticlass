from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . serializers import *
from . models import *
from django.shortcuts import get_object_or_404
import google.generativeai as genai
import statistics

# Create your views here.

# USER VIEWS
# User Views are the only ones that should use auth_id, easier to manage foreign key relationships off integer primary keys
# Even if you set auth_id as a pk, it makes it more complicated than it needs to be. 
class UserListView(APIView):
    
    #Technically not secure, shouldn't have access to other user's auth_id or personal information. 
    #Helpful for testing though. 
    def get(self, request):
        users = User.objects.filter()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):

    # Get request 200 found, 404 not found
    def get(self, request, auth_id):
        user_instance = get_object_or_404(User, auth_id=auth_id)
        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Post request 201 created, 400 data invalid
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, auth_id):
        user = get_object_or_404(User, auth_id=auth_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, auth_id):
        user = get_object_or_404(User, auth_id=auth_id)
        user.delete()
        return Response({"message": f"User '{auth_id}' deleted"}, status=status.HTTP_204_NO_CONTENT)

# COURSE VIEWS
class CourseListView(APIView):
    
    # Course List View is just listing all the courses, so no need to filter name, its not being used like that in any url. 
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = CourseSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    
    def get(self, request, course_id):
        
        course = get_object_or_404(Course, pk=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        serializer = CourseSerializer(course, data=request.data)
        
        #This is fine, although, if theres an update needed, we will probably just send everything. 
        if serializer.is_valid():
            if 'name' in request.data:
                new_name = request.data.get('name')
                course.name = new_name

            if 'status' in request.data:
                new_status = request.data.get('status')
                course.status = new_status

            if 'instructor' in request.data:
                user_id = request.data.get('instructor')
                
                try:
                    user = User.objects.get(auth_id=user_id)
                except User.DoesNotExist:
                    return Response({"error": f"User '{user_id}' not found"}, status=status.HTTP_404_NOT_FOUND)
                
                course.instructor = user
            
            if 'description' in request.data:
                new_description = request.data.get('description')
                course.description = new_description
                
            if 'course_image' in request.data:
                new_course_image = request.data.get('course_image')
                course.course_image = new_course_image

            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        return Response({"message": f"Course '{course.name}' deleted"}, status=status.HTTP_204_NO_CONTENT)

# ENROLLMENT VIEWS
class CourseEnrollmentListView(APIView):
    
    def get(self, request, user_id):
        
        enrollments = Enrollment.objects.filter(user__id=user_id)
        
        course_data = []
        
        for enrollment in enrollments:
            course = enrollment.course
            grade = enrollment.grade
            
            serialized_course = CourseSerializer(course).data
            serialized_course["grade"] = grade
            course_data.append(serialized_course)
            
        return Response(course_data, status=status.HTTP_200_OK)

class CreateEnrollment(APIView):
    
    def post(self, request):
        # Deserialize the request data
        serializer = EnrollmentSerializer(data=request.data)
    
        # Check if the data is valid
        if serializer.is_valid():
            # Save the enrollment
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# ASSIGNMENT VIEWS
# For testing so we can see all the assignments, in reality, only need assignments that correspond to a single course. 
class TestAssignmentListView(APIView):
    
    def get(self, request):
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentListView(APIView):
    
    def get(self, request, course_id):
        assignments = Assignment.objects.filter(course=course_id)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, course_id):
        
        serializer = AssignmentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentDetailView(APIView):
    
    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        assignment.delete()
        return Response({"message": f"Assignment '{assignment.title}' deleted"}, status=status.HTTP_204_NO_CONTENT)


class UserAssignmentListView(APIView):
    
    def get(self, request, course_id):
        #Get the user id as a query param
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({"error":'Must provide user id.'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Filter for all assignments with given course id
        assignments = Assignment.objects.filter(course=course_id)
        serialized_data = []
        
        #For each assignment in this list of assignments, append the corresponding user data if its present. 
        for assignment in assignments:
            
            serialized_assignment = AssignmentSerializer(assignment).data
            
            #Get user data for the assignment
            user_assignment = UserAssignment.objects.filter(assignment=assignment, user=user_id).first()
            
            # Store user data in serialized assignment
            if user_assignment:
                serialized_assignment['grade'] = user_assignment.grade
                serialized_assignment['is_complete'] = user_assignment.is_complete
            else:
                return Response({"error":'No user data associated with assignments.'}, status=status.HTTP_400_BAD_REQUEST)
                

            #Get activity information for the assignment
            activities = Activity.objects.filter(assignment=assignment)
            serialized_activities = []
            
            #For each activity in the assignment
            for activity in activities:
                
                #Serialize the activity
                serialized_activity = ActivitySerializer(activity).data
                
                #Get the user's activity
                user_activity = UserActivity.objects.filter(activity=activity, user=user_id).first()
                
                #Store user data in serialized activity
                if user_activity:
                    serialized_activity['grade'] = user_activity.grade
                    serialized_activity['is_complete'] = user_activity.is_complete
                else:
                    return Response({"error":'No user data associated with this activity.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Append to serialized activities
                serialized_activities.append(serialized_activity)
            
            #Put all activity data within the assignment. 
            serialized_assignment['activities'] = serialized_activities
            
            serialized_data.append(serialized_assignment)
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class UserAssignmentDetailView(APIView):
    
    def get(self, request, assignment_id):
        #Get the user id as a query param
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({"error":'Must provide user id.'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(assignment_id)
        #Filter for all assignments with given assignment id
        assignment = get_object_or_404(Assignment, pk=assignment_id)
            
        #Get user data for the assignment
        user_assignment = UserAssignment.objects.filter(assignment=assignment, user=user_id).first()
            
        serialized_assignment = AssignmentSerializer(assignment).data
        
        #I actually want to include the course name info too 
        serialized_assignment['course_name'] = assignment.course.name
            
        # Store user data in serialized assignment
        if user_assignment:
            serialized_assignment['grade'] = user_assignment.grade
            serialized_assignment['is_complete'] = user_assignment.is_complete
        else:
            return Response({"error":'No user data associated with this assignment.'}, status=status.HTTP_400_BAD_REQUEST)
            

        #Get activity information for the assignment
        activities = Activity.objects.filter(assignment=assignment)
        serialized_activities = []
        
        #For each activity in the assignment
        for activity in activities:
            
            #Serialize the activity
            serialized_activity = ActivitySerializer(activity).data
            
            #Get the user's activity
            user_activity = UserActivity.objects.filter(activity=activity, user=user_id).first()
            
            #Store user data in serialized activity
            if user_activity:
                serialized_activity['grade'] = user_activity.grade
                serialized_activity['is_complete'] = user_activity.is_complete
            else:
                return Response({"error":'No user data associated with this activity.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Append to serialized activities
            serialized_activities.append(serialized_activity)
        
        #Put all activity data within the assignment. 
        serialized_assignment['activities'] = serialized_activities
        
        return Response(serialized_assignment, status=status.HTTP_200_OK)
    

# ACTIVITIES VIEWS
class TestActivityListView(APIView):
    
    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActivityListView(APIView):
    def get(self, request, assignment_id):
        activities = Activity.objects.filter(assignment=assignment_id)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, assignment_id):
        serializer = ActivitySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivityDetailView(APIView):
    
    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        serializer = ActivitySerializer(activity, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        activity.delete()
        return Response({"message": f"Activity '{activity.title}' deleted"}, status=status.HTTP_204_NO_CONTENT)


# QUESTION VIEWS
class TestQuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class QuestionListView(APIView):
    
    def get(self, request, activity_id):
        questions = Question.objects.filter(activity=activity_id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, activity_id):
        
        serializer = QuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionDetailView(APIView):
    
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response({"message": f"Activity '{question.question}' deleted"}, status=status.HTTP_204_NO_CONTENT)



# class CourseGradeView(APIView):
#     def calculate_and_update_grade(self, user, course):
#         assignments = Assignment.objects.filter(course_id=course.id)
#         assignment_grades = []
#         for assignment in assignments:
#             try:
#                 assignment_grade = AssignmentGrade.objects.get(auth_id=user, course_id=course.id, assignment_id=assignment.id).grade
#                 assignment_grades.append(assignment_grade)
#             except AssignmentGrade.DoesNotExist:
#                 return Response({"error": f"Grade not found for assignment {assignment.id}"}, status=status.HTTP_404_NOT_FOUND)

#         average_grade = statistics.mean(assignment_grades) if assignment_grades else 0

#         # Update or create CourseGrade instance
#         course_grade, _ = CourseGrade.objects.update_or_create(
#             auth_id=user,
#             course_id=course,
#             defaults={'grade': average_grade}
#         )
#         serializer = CourseGradeSerializer(course_grade)
#         return serializer.data

#     def get(self, request, course_name):
#         user_id = request.query_params.get('auth_id')
#         try:
#             user = User.objects.get(auth_id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         try:
#             course = Course.objects.get(name=course_name)
#         except Course.DoesNotExist:
#             return Response({"error": "Course not found"}, status=status.HTTP_400_BAD_REQUEST)

#         # Calculate and update grade
#         course_grade_data = self.calculate_and_update_grade(user, course)
#         return Response(course_grade_data)
            

# More complicated than it needs to be. Reused some of this in refactored enrollment view

# class UserEnrollmentView(APIView):
#     def get(self, request):
#         user = request.query_params.get('auth_id')
#         if user:
#             try:
#                 user_obj = get_object_or_404(User, auth_id=user)
#                 user_courses = user_obj.course_set.all()
#                 courses_data = []
#                 for course in user_courses:
#                     try:
#                         grade_obj = CourseGrade.objects.get(auth_id=user_obj, course_id=course.id)
#                         grade = grade_obj.grade
#                     except CourseGrade.DoesNotExist:
#                         grade = None
#                         print(f"No CourseGrade entry found for user {user_obj.auth_id} and course {course.id}")

#                     course_data = {
#                         "course_id": course.id,
#                         "name": course.name,
#                         "grade": grade
#                     }
#                     courses_data.append(course_data)
#                 return Response(courses_data)
#             except User.DoesNotExist:
#                 return Response({"error": "User not found"}, status=404)
#         else:
#             return Response({"error": "User ID required"}, status=400)


#Easier to just delete an Enrollment object or set it to inactive. 
# class RemoveUsersFromCourseView(APIView):
    
#     # No need to have a get request for this view. 
#     def get(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseSerializer(course)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         try:
#             course = Course.objects.get(pk=pk)
#         except Course.DoesNotExist:
#             return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Get the email(s) to remove
#         user_ids = request.data['users']
#         if not user_ids:
#             return Response({"error": "ID(s) of the user(s) to be removed is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # If a single email is provided, convert it to a list
#         if isinstance(user_ids, str):
#             user_ids = [user_ids]

#         remove_messages = []
#         error_messages = []

#         # Iterate over each email and remove the corresponding student
#         for user_id in user_ids:
#             try:
#                 user = User.objects.get(auth_id=user_id)
#                 course.users.remove(user)
#                 remove_messages.append(
#                     f"User '{user_id}' removed from course '{course.name}'")
#             except User.DoesNotExist:
#                 error_messages.append(f"User '{user_id}' not found")

#         # Construct response message
#         message = {
#             "message": remove_messages,
#             "errors": error_messages
#         }

#         return Response(message, status=status.HTTP_200_OK)


# class AssignmentListView(APIView):
#     def get(self, request):
#         course_name = request.query_params.get('course_name')
#         if course_name:
#             try:
#                 ## Like here its way easier to just pass in the course id. Avoid the problem below. 
#                 course = Course.objects.get(name=course_name)
#                 assignments = Assignment.objects.filter(course_id=course)
#                 serializer = AssignmentSerializer(assignments, many=True)
#                 url = reverse('course_assignment_view', kwargs={'course_name': course_name})
#                 return redirect(url)
#             except Course.DoesNotExist:
#                 return Response({"error": "Course not found"}, status=404)
#         else:
#             #Always need some filtering, no need outside testing to get a list of all assignments. 
#             assignments = Assignment.objects.all()
#             serializer = AssignmentSerializer(assignments, many=True)
#             return Response(serializer.data)

#     def post(self, request):
#         serializer = AssignmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AssignmentDetailView(APIView):
#     def get(self, request, pk):
#         assignment = get_object_or_404(Assignment, pk=pk)
#         serializer = AssignmentSerializer(assignment)
#         return Response(serializer.data)

#     def put(self, request, pk):

#         assignment = get_object_or_404(Assignment, pk=pk)

#         serializer = AssignmentSerializer(assignment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):

#         assignment = get_object_or_404(Assignment, pk=pk)
#         assignment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class CourseAssignmentListView(APIView):
#     def get(self, request, course_name):
#         course = get_object_or_404(Course, name=course_name)
#         assignments = Assignment.objects.filter(course_id=course)
#         serializer = AssignmentSerializer(assignments, many=True)
#         return Response(serializer.data)
    

# class AssignmentGradesByCourseView(APIView):
#     def get(self, request, course_name):
#         user_id = request.query_params.get('auth_id')
#         user = User.objects.get(auth_id=user_id)
#         if user:
#             try:
#                 course = Course.objects.get(name=course_name)
#                 if not course:
#                     return Response({"error": "Course not found"}, status=status.HTTP_400_BAD_REQUEST)
                
#                 assignments = Assignment.objects.filter(course_id=course.id)
#                 assignment_grades = []
#                 for assignment in assignments:
#                     try:
#                         assignment_grade = AssignmentGrade.objects.get(auth_id=user, course_id=course.id, assignment_id=assignment.id).grade
#                         assignment_grade_data = {
#                             "assignment_id": assignment.id,
#                             "grade": assignment_grade
#                         }
#                         assignment_grades.append(assignment_grade_data)
#                     except AssignmentGrade.DoesNotExist:
#                         return Response({"error": f"Grade not found for assignment {assignment.id}"}, status=status.HTTP_404_NOT_FOUND)

#                 return Response(assignment_grades)
#             except AssignmentGrade.DoesNotExist:
#                 return Response({"error": "Grade not found"}, status=404)
#         else:
#             return Response({"error": "User ID required"}, status=400)
    

# class AssignmentGradeView(APIView):
#     @staticmethod
#     def calculate_assignment_grade(assignment_id):
#         # Retrieve all AssignmentQuestion instances for the given assignment_id
#         assignment_questions = AssignmentQuestion.objects.filter(assignment_id=assignment_id)
        
#         # Count the number of questions and correctly answered questions
#         total_questions = len(assignment_questions)
#         correctly_answered_questions = sum(question.answered_correctly for question in assignment_questions)
        
#         # Calculate the grade (percentage of correctly answered questions)
#         grade = (correctly_answered_questions / total_questions) * 100 if total_questions > 0 else 0
        
#         return grade

#     def get(self, request, course_name, assignment_id):
#         user_id = request.query_params.get('auth_id')
        
#         try:
#             user = User.objects.get(auth_id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         try:
#             course = Course.objects.get(name=course_name)
#             assignment = Assignment.objects.get(id=assignment_id, course_id=course.id)
#         except (Course.DoesNotExist, Assignment.DoesNotExist):
#             return Response({"error": "Course or Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         # Calculate the grade for the assignment
#         assignment_grade = self.calculate_assignment_grade(assignment_id)
        
#         # Update or create AssignmentGrade instance
#         assignment_grade_obj, _ = AssignmentGrade.objects.update_or_create(
#             auth_id=user,
#             course_id=course,
#             assignment_id=assignment,
#             defaults={'grade': assignment_grade}
#         )
        
#         # Serialize the AssignmentGrade instance
#         serializer = AssignmentGradeSerializer(assignment_grade_obj)
#         return Response(serializer.data)


# class AssignmentQuestionListView(APIView):

#     def get(self, request):
#         assignments_questions = AssignmentQuestion.objects.all()
#         serializer = AssignmentQuestionSerializer(
#             assignments_questions, many=True)
#         return Response(serializer.data)

#     def post(self, request):

#         serializer = AssignmentQuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AssignmentQuestionDetailView(APIView):

#     def get(self, request, assignment_id, question_id):
#         assignments_questions = get_object_or_404(AssignmentQuestion, assignment_id=assignment_id, question_id=question_id)
#         serializer = AssignmentQuestionSerializer(assignments_questions)
#         return Response(serializer.data)

#     def put(self, request, assignment_id, question_id):
#         assignments_questions = get_object_or_404(AssignmentQuestion, assignment_id=assignment_id, question_id=question_id)

#         serializer = AssignmentQuestionSerializer(
#             assignments_questions, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, assignment_id, question_id):
#         assignments_questions = get_object_or_404(AssignmentQuestion, assignment_id=assignment_id, question_id=question_id)
#         assignments_questions.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    
# class AssignmentQuestionByIDView(APIView):
#     def get(self, request, assignment_id):
#         assignment_questions = AssignmentQuestion.objects.filter(assignment_id=assignment_id).all()
#         if not assignment_questions:
#             return Response({"error": "Assignment not found."}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = AssignmentQuestionSerializer(assignment_questions, many=True)
#         return Response(serializer.data)


# class QuestionListView(APIView):

#     def get(self, request):
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)

#     def post(self, request):

#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class QuestionDetailView(APIView):

#     def get(self, request, pk):
#         questions = get_object_or_404(Question, pk=pk)
#         serializer = QuestionSerializer(questions)
#         return Response(serializer.data)

#     def put(self, request, pk):

#         questions = get_object_or_404(Question, pk=pk)

#         serializer = QuestionSerializer(questions, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):

#         questions = get_object_or_404(Question, pk=pk)
#         questions.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class AlternateQuestionListView(APIView):

#     def get(self, request):
#         alt_questions = AlternateQuestion.objects.all()
#         serializer = AlternateQuestionSerializer(alt_questions, many=True)
#         return Response(serializer.data)

#     def post(self, request):

#         serializer = AlternateQuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AlternateQuestionDetailView(APIView):

#     def get(self, request, pk):
#         alt_questions = get_object_or_404(AlternateQuestion, pk=pk)
#         serializer = AlternateQuestionSerializer(alt_questions)
#         return Response(serializer.data)

#     def put(self, request, pk):

#         alt_questions = get_object_or_404(AlternateQuestion, pk=pk)

#         serializer = AlternateQuestionSerializer(
#             alt_questions, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):

#         alt_questions = get_object_or_404(AlternateQuestion, pk=pk)
#         alt_questions.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ChatbotView(APIView):
    def post(self, request):
        chat_prompt = request.data.get('question')

        if chat_prompt is None:
            return Response({'error': 'Question is required.'}, status=status.HTTP_400_BAD_REQUEST)

        genai.configure(api_key="AIzaSyBIKvpvW6-RDwXMorDKCs-EJv8bBgmYxPo")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
        ]
        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        directions = "For the given Algebra 1 problem, illustrate each step towards finding the solution. Provide a concise text explanation for what each step accomplishes, aiming for clarity and brevity. It's crucial to demonstrate the process without skipping directly to the solution. If the following problem is not related to Math, please respond kindly prompting the student to stay on topic. Problem: "
        full_prompt = directions + chat_prompt
        prompt_parts = [{"text": full_prompt}]
        response = model.generate_content(prompt_parts)

        if response.parts:
            return Response({'solution': response.parts[0].text}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No response generated or the prompt was blocked.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
class ProblemGeneratorView(APIView):
    def post(self, request):
        chat_prompt = request.data.get('question')
        genai.configure(api_key="AIzaSyBIKvpvW6-RDwXMorDKCs-EJv8bBgmYxPo")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
        ]
        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        directions = "For the given Algebra 1 problem, provide one similar but different problem with the same type, format, and difficulty. give the problem and the answer. they should be clearly labled Problem: put_problem_here Answer: put_answer_here. If the current problem is not related to math, respond with the word 'No' and nothing else - I need this for error handling. Current Problem: "
        full_prompt = directions + chat_prompt
        prompt_parts = [{"text": full_prompt}]
        response = model.generate_content(prompt_parts)
        
        if response.parts:
            response_text = response.parts[0].text
            if response_text == "No":
                return Response({'error': 'The provided problem is not related to Algebra 1.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                problem_start = response_text.find("Problem: ") + len("Problem: ")
                answer_start = response_text.find("Answer: ") + len("Answer: ")
                if problem_start > len("Problem: ") - 1 and answer_start > len("Answer: ") - 1:
                    problem_end = response_text.find("Answer: ") - 1
                    answer_end = len(response_text)
                    problem = response_text[problem_start:problem_end].strip()
                    answer = response_text[answer_start:answer_end].strip()
                    return Response({'question': problem, 'answer': answer}, status=status.HTTP_200_OK)
                else:
                    raise ValueError('Parsing error')
            except ValueError:
                return Response({'error': 'Error parsing the response.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No response generated or the prompt was blocked.'}, 
                            status=status.HTTP_400_BAD_REQUEST)


# Engagement Data Views
class EngagementDataAPIView(APIView):
    def get(self, request):
        try:
            all_data = EngagementData.objects.all()
            serializer = EngagementDataSerializer(all_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EngagementData.DoesNotExist:
            return Response({'error': 'No engagement data'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = EngagementDataSerializer(data=request.data)
        if serializer.is_valid():
            engagement_data = serializer.save()
            
            # Assuming engagement_periods data is present in request.data
            period_data = request.data.get('engagement_periods', [])
            period_serializer = EngagementPeriodSerializer(data=period_data, many=True, context={'engagement_data': engagement_data})
            
            if period_serializer.is_valid():
                period_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)