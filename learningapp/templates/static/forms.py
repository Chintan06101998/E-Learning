import datetime
import json

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from django import forms
from django.forms import ModelForm

from learningapp.models import Course, Users, Material, Assignment, Result, AssignmentAnswer, Result


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
        fields = ['name','description']

class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']

class addMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields =['name','description','document']

class addAssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['name','description','document','due_date','due_time','grade']
        widgets = {
            'due_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            ),
            'due_time': forms.DateInput(
                attrs={'type': 'time', 'placeholder': 'HH:MM:SS', 'class': 'form-control'}
            )
        }

class addMarksForms(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['grade']
        # widgets = {
        #     'due_date': forms.DateInput(
        #         attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
        #     ),
        #     'due_time': forms.DateInput(
        #         attrs={'type': 'time', 'placeholder': 'HH:MM:SS', 'class': 'form-control'}
        #     )


class uploadAnswerForm(forms.ModelForm):
    class Meta:
        model = AssignmentAnswer
        fields = "__all__"

class GradeForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = "__all__"

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['question_text','marks']
#
#
# QuestionFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm, extra=1)
#
# class AddQuizForm(forms.ModelForm):
#     class Meta:
#         model = Quiz
#         fields = ['quiz_name', 'duration']
#
#
#
# class UpdateQuizForm(forms.ModelForm):
#     class Meta:
#         model = Quiz
#         fields = ['quiz_name', 'duration']


