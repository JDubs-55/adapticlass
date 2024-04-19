from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Enrollment)
# admin.site.register(CourseGrade)
admin.site.register(Assignment)
admin.site.register(UserAssignment)
admin.site.register(Activity)
admin.site.register(UserActivity)

# admin.site.register(AssignmentGrade)
# admin.site.register(AssignmentQuestion)
admin.site.register(Question)
admin.site.register(UserQuestion)
# admin.site.register(AlternateQuestion)
admin.site.register(Chat)
admin.site.register(EngagementData)
admin.site.register(EngagementPeriod)