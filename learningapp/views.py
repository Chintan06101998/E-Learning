from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from learningapp.models import Course
from learningapp.templates.static.forms import CreateUserForm, CreateCourseForm, UpdateCourseForm


# def login(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request,user)
#             return  JsonResponse({"message":"Login Successfully"})
#         else :
#             return JsonResponse({"message":"Username & Password are invalid"})

def register(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'register.html', context)
