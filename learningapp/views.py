from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

from learningapp.models import Course, Material
from learningapp.templates.static.forms import UserRegistrationForm, LoginForm
from .models import Users  # Import your custom User model


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


def home_tutor(request):

    return render(request, 'tutors/home.html' )

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate using your custom User model
            try:
                user = Users.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)

                    # Access custom fields of the User model here
                    user_type = user.user_type
                    memberShip = user.memberShip
                    if(int(user_type)!=0):
                        #render student view
                        form = LoginForm()
                        render(request, 'login.html', {'form': form})
                    else:
                        return render(request,'tutors/home.html',{'user':user})
                        #render tutor view
                   
            except Users.DoesNotExist:
                return form.add_error(None, 'No such user exists.')
        else:
            return form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def getmaterial(request, course_id):
    material = Material.objects.filter(course_id=course_id)
    return render(request, 'getcourses.html',{'material':material})
