"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',  views.login_view),
    path('register/',  views.register, name="register"),
    path('login/',  views.login_view ,name="login"),
    path('getmaterial/<int:course_id>', views.getmaterial),
    path('tutors/',include('learningapp.tutors.urls')),
    path('students/',include('learningapp.students.urls')),
    path('logout/',views.logout_view,name='logout'),
    path('checkout/<str:selected_membership>/<int:user_id>/', views.checkout, name='checkout'),
    path('rs/<str:selected_membership>/<int:user_id>', views.registration_success, name='rs'),
    path('cp/<int:user_id>', views.cancel_plan, name='cancel-plan'),
    path('grade_view/',views.grade_view,name='Grade View'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
