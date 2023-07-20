from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from learningapp.models import Course, Material
from learningapp.templates.static.forms import UserRegistrationForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("form--->>", str(form))
        if form.is_valid():
            form.save()
            # Redirect to a success page or perform other actions
            return HttpResponse('success')
        else:
            return HttpResponse("Error")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return HttpResponse('Login Successfully')
            else:
                # Handle invalid credentials
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def getmaterial(request, course_id):
    material = Material.objects.filter(course_id=course_id)
    return render(request, 'getcourses.html',{'material':material})
