import datetime

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from learningapp.models import Course, Users, Material, Assignment


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'memberShip']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any additional form customization or validation here


class LoginForm(AuthenticationForm):
    class Meta:
        model = Users
        fields = ['username', 'password']


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','description','tutor']

class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']

class addMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

class addAssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = '__all__'
        widgets = {
            'due_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            ),
            'due_time': forms.DateInput(
                attrs={'type': 'time', 'placeholder': 'HH:MM:SS', 'class': 'form-control'}
            )
        }