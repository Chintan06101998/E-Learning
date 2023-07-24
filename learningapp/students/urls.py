
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('uploadanswer/<int:assignment_id>',views.uploadAnswer),
    path('home', views.home_student ,name = "student-home"),
    path('courses', views.getEnrolledCourses, name = "student-courses"),
    path('browse-courses', views.getAvailableCourses, name = "student-browse-courses"),
    path('enroll-course/<int:course_id>', views.enrollCourse, name = "student-enroll-course"),

    path('getallcourses',views.getallcourse),
    path('assignment-submit/<int:assignment_id>', views.assignment_submission, name='assignment-submission'),
    path('course-details/<int:course_id>', views.view_course_details, name='view-course-details'),
    path('course-assignment/<int:course_id>', views.viewCourseAssignments, name='course-assignment'),
    path('view-assignment/<int:course_id>', views.view_materials, name='view-assignment')
]
