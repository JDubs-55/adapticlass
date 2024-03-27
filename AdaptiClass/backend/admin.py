from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentQuestion)
admin.site.register(Question)
admin.site.register(AlternateQuestion)
admin.site.register(Chat)