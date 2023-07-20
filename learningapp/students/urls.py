
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('getallcourses',views.getallcourse),
    path('uploadanswer/<int:assignment_id>',views.uploadAnswer)
]
