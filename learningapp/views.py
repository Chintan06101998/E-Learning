from random import random

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from learningapp.models import  AssignmentAnswer
from django.contrib.auth import  login
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from learningapp.models import Course, ClassMaterial
from learningapp.templates.static.forms import UserRegistrationForm, UserLoginForm, GradeForm
from .models import Users
from django.core.mail import send_mail

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("form--->>", str(form))
        if form.is_valid():
            form.save()
            # Redirect to a success page or perform other actions
            return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponse("Error")
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})



def logIn(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate using your custom User model
            try:
                user = Users.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)
                    request.session['user'] = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'usertype': user.user_type,
                        'membership': user.memberShip
                        # Add any other user-related data you need
                    }
                    # Access custom fields of the User model here
                    user_type = user.user_type
                    memberShip = user.memberShip
                    if int(user_type) == 0:
                        # render student view
                        form = UserLoginForm()
                        response = HttpResponseRedirect(reverse("student-home"))
                        return response
                    else:
                        return HttpResponseRedirect(reverse('tutor-home'))
                        # render tutor view
            except Users.DoesNotExist:
                form.add_error(None, 'No such user exists.')
        else:
            form.add_error(None, 'Invalid username or password')
    else:
        if not request.session.is_empty():
            if('user' in request.session):
                user = request.session['user']
                print(user)
                if int(user['usertype']) == 0:
                    # render student view
                    form = UserLoginForm()
                    response = HttpResponseRedirect(reverse("student-home"))
                    return response
                else:
                    # render tutor view
                    return HttpResponseRedirect(reverse('tutor-home'))
                  
            else:
                 form = UserLoginForm()
        else:
            form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

# def forgotPassword(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         user = get_object_or_404(Users, email = email)
#         if user:
#
#             otp = random.randrange(100000, 999999)
#             send_email(otp, user.email)
#             HttpResponse("Email sent successfully!")
#
#         print("form--->>", str(form))
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or perform other actions
#             return HttpResponseRedirect(reverse('login'))
#         else:
#             return HttpResponse("Error")
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'registration.html', {'form': form})

def send_email(otp,recipient_email):
    subject = 'Reset Password OTP'
    message = 'This is a OTP ' + otp + ' to reset password on Enlight Learn'
    from_email = 'chintan090298@gmail.com'  # Replace with your email address
    recipient_list = [recipient_email]  # Replace with the recipient's email address

    send_mail(subject, message, from_email, recipient_list)
    return


def getClassMaterials(request, course_id):
    material = ClassMaterial.objects.filter(course_id=course_id)
    return render(request, 'getcourses.html', {'material':material})

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def grade(request, course_id, assignment_id):
    course = Course.objects.get(pk=1)
    assignmentAnswer = AssignmentAnswer.objects.filter(course=course)


    if request.method == 'POST':
        form = GradeForm(request, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Grade")
    else:
        form = GradeForm()

        return render(request, 'tutors/grade.html', {'form':form})


