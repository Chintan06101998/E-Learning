
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('createcourse/', views.createCourse),
    path('updatecourse/<int:course_id>/', views.updateCourse),
    path('deletecourse/<int:course_id>/', views.deleteCourse, name='delete_course'),
    path('addmaterial/',views.addMaterial),
    path('updatematerial/<int:material_id>', views.updateMaterial),
    path('deletematerial/<int:material_id>', views.deleteMaterial),
    path('addassignment/', views.addAssignment),
    path('updateassignment/<int:assignment_id>', views.updateAssignment),
    path('deleteassignment/<int:assignment_id>', views.deleteAssignment),
    path('home', views.home_tutor, name = "tutor-home"),
    path('courses/', views.getcourse, name = "tutor-courses"),
    path('addmarks/', views.addMarks),
    path('createquiz/', views.createquiz),
    path('updatequiz/<int:quiz_id>', views.updateQuiz)
]
