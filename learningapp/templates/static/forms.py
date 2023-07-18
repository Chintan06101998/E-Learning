import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from learningapp.models import Course, Users, Material, Assignment


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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