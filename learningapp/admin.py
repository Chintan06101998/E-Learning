from django.contrib import admin

from .models import Users, Course, Material, Quiz, Results, AssignmentAnswer,Subscription,Grade, Assignment, Question, Option
from .models import Users, Course, Material, Quiz, Results, AssignmentAnswer,Subscription,Grade, Assignment, StudentCourses

# Register your models here.

admin.site.register(Users)
admin.site.register(Course)
admin.site.register(Material)

admin.site.register(Results)
admin.site.register(AssignmentAnswer)
admin.site.register(Subscription)
admin.site.register(Grade)
admin.site.register(Quiz)
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Option)


admin.site.register(StudentCourses)

