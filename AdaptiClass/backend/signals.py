from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.db.models import Avg


@receiver(post_save, sender=Assignment)
def create_user_assignments(sender, instance, created, **kwargs):
    if created:
        # Get all users enrolled in the course
        users = instance.course.enrollment_set.all()
        # Create a UserAssignment object for each user
        for user_enrollment in users:
            user_assignment = UserAssignment.objects.create(user=user_enrollment.user, assignment=instance)
        
@receiver(post_save, sender=Activity)
def create_user_activities(sender, instance, created, **kwargs):
    if created:
        # Get all users enrolled in the course
        users = instance.assignment.course.enrollment_set.all()
        # Create a UserActivity object for each user
        for user_enrollment in users:
            user_activity = UserActivity.objects.create(user=user_enrollment.user, activity=instance)
            
        
@receiver(post_save, sender=Question)
def create_user_questions(sender, instance, created, **kwargs):
    if created:
        # Get all users enrolled in the course
        users = instance.activity.assignment.course.enrollment_set.all()
        # Create a UserQuestion object for each user
        for user_enrollment in users:
            user_question = UserQuestion.objects.create(user=user_enrollment.user, question=instance)



@receiver(post_save, sender=Enrollment)
def create_user_objects(sender, instance, created, **kwargs):
    if created:
        # Get all assignments for the enrolled course
        assignments = instance.course.assignment_set.all()

        # Iterate over each assignment
        for assignment in assignments:
            
            UserAssignment.objects.create(user=instance.user, assignment=assignment)
            
            # Get all activities for the current assignment
            activities = assignment.activity_set.all()

            # Iterate over each activity within the assignment
            for activity in activities:
                # Create a UserActivity object for the user and the current activity
                UserActivity.objects.create(user=instance.user, activity=activity)
                
                questions = activity.question_set.all()
                
                for question in questions:
                    
                    UserQuestion.objects.create(user=instance.user, question=question)


@receiver([post_save, post_delete], sender=UserActivity)
def update_grades(sender, instance, **kwargs):
    # Get the user associated with the UserActivity
    user = instance.user

    # Update UserAssignment grade
    update_user_assignment_grade(instance)

    # Update Enrollment grade
    update_enrollment_grade(instance)

def update_user_assignment_grade(user_activity):
    # Get the related assignment
    assignment = user_activity.activity.assignment
    
    # Get the related UserAssignment object for the assignment and user. 
    user_assignment = UserAssignment.objects.get(user=user_activity.user, assignment=assignment)

    # Get the related activities in assignment
    activities = Activity.objects.filter(assignment=assignment)
    
    # Get the UserActivities associated with the assignment. 
    user_activities = UserActivity.objects.filter(activity__in=activities, user=user_activity.user, is_complete=True)
    
    # Calculate the average grade of all activities for the user within the same assignment
    average_grade = user_activities.aggregate(average_grade=Avg('grade'))['average_grade']
    
    # Set the calculated grade. 
    user_assignment.grade = average_grade
    user_assignment.save(update_fields=['grade'])

def update_enrollment_grade(user_activity):
    #Get the course
    course = user_activity.activity.assignment.course
    # Get all the assignments related to the course
    assignments = Assignment.objects.filter(course=course)
    
    # Get the enrollment object
    enrollment = Enrollment.objects.get(user=user_activity.user, course=course)
    
    user_assignments = UserAssignment.objects.filter(assignment__in=assignments, user=user_activity.user, is_complete=True)

    # Calculate the total grade of all assignments for the user within the course
    total_grade = user_assignments.aggregate(average_grade=Avg('grade'))['average_grade']

    # Update the grade of the Enrollment object for the user and course
    enrollment.grade = total_grade
    enrollment.save(update_fields=['grade'])