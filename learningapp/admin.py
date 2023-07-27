from django.contrib import admin
from .models import Users, Course, ClassMaterial, Result, AssignmentAnswer, Subscription, Grade, Assignment, StudentCourses

admin.site.register(Users)
admin.site.register(Course)
admin.site.register(ClassMaterial)
admin.site.register(Result)
admin.site.register(AssignmentAnswer)
admin.site.register(Subscription)
admin.site.register(Grade)
admin.site.register(Assignment)
admin.site.register(StudentCourses)