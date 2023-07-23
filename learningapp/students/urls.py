
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('uploadanswer/<int:assignment_id>',views.uploadAnswer),
    path('home', views.home_student ,name = "student-home"),
    path('courses', views.getEnrolledCourses, name = "student-courses"),
    path('browse-courses', views.getAvailableCourses, name = "student-browse-courses"),
    path('enroll-course/<int:course_id>', views.enrollCourse, name = "student-enroll-course"),

]
