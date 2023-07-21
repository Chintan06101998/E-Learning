
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('create-course/', views.createCourse,name="tutor-add-course"),
    path('view-course/<int:course_id>/', views.viewCourse,name="tutor-view-course"),
    path('view-course-material/<int:course_id>/', views.viewCourseMaterials,name="tutor-view-course-material"),
    path('view-course-assignments/<int:course_id>/', views.viewCourseAssignments,name="tutor-view-course-assignments"),
    path('view-course-quizzes/<int:course_id>/', views.viewCourseQuizzes,name="tutor-view-course-quizzes"),
    path('edit-course/<int:course_id>/', views.updateCourse,name='tutor-edit-course'),
    path('delete-course/<int:course_id>/', views.deleteCourse, name='tutor-delete-course'),
    path('create-course-material/<int:course_id>',views.addMaterial,name='tutor-add-course-material'),
    path('edit-course-material/<int:material_id>', views.updateMaterial,name='tutor-edit-course-material'),
    path('delete-course-material/<int:material_id>', views.deleteMaterial,name='tutor-delete-course-material'),
    path('create-course-assignment/<int:course_id>/', views.addAssignment,name='tutor-add-course-assignment'),
    path('edit-course-assignment/<int:assignment_id>', views.updateAssignment,name='tutor-edit-course-assignment'),
    path('delete-course-assignment/<int:assignment_id>', views.deleteAssignment,name='tutor-delete-course-assignment'),
    path('home', views.home_tutor, name = "tutor-home"),
    path('courses', views.getcourse, name = "tutor-courses"),
    path('addmarks/', views.addMarks),
    path('createquiz/', views.createquiz),
    path('updatequiz/<int:quiz_id>', views.updateQuiz)
]
