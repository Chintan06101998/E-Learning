from django.contrib import admin

from .models import Users, Course, Material, Quiz,Question,Option, Results, MaterialAnswer,Subscription,Grade, Assignment

# Register your models here.

admin.site.register(Users)
admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Results)
admin.site.register(MaterialAnswer)
admin.site.register(Subscription)
admin.site.register(Grade)
admin.site.register(Quiz)
admin.site.register(Assignment)

