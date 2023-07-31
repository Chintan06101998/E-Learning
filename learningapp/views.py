from django.contrib.auth import login, logout
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from learningapp.models import Material, Users, Assignment, AssignmentAnswer
from learningapp.models import Material, Users
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

from learningapp.models import Course, Material
from learningapp.templates.static.forms import UserRegistrationForm, LoginForm, GradeForm
from .models import Users  # Import your custom User model
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("form--->>", str(form))
        selected_membership = form.cleaned_data['memberShip']
        form.cleaned_data['memberShip'] = 'F'  
        if form.is_valid():      
            user  = form.save()
            user_id = user.id  # Get the ID of the user
            if selected_membership != 'F':
                return HttpResponseRedirect(reverse('checkout',args=[selected_membership,user_id]))
            else:
                # If free membership, create the user and complete the registration  
                return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponse("Error")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def checkout(request,selected_membership,user_id):
    if selected_membership == 'P':
        # You can add more plans and their respective Stripe plan IDs here
        stripe_plan_id = 'price_1NXFSzHNGyeJCpDlr4hbObs9'
    elif  selected_membership == 'G':
        # You can add more plans and their respective Stripe plan IDs here
        stripe_plan_id = 'price_1NXFRnHNGyeJCpDlX0FMNmwL'
    elif  selected_membership == 'S':
        # You can add more plans and their respective Stripe plan IDs here
        stripe_plan_id = 'price_1NXFQZHNGyeJCpDlHjAqEOfV' 


    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': stripe_plan_id,
            'quantity': 1,
        }],
        mode='payment',  # Use 'payment' for one-time payments
        success_url=request.build_absolute_uri(reverse('rs',args=[selected_membership,user_id])),
    )

    return HttpResponseRedirect(session.url)


def registration_success(request,selected_membership,user_id):

    user = get_object_or_404(Users, id=user_id)
    user.memberShip = selected_membership  # Assuming the membership field is called 'memberShip'
    user.save()
    # Redirect to a success page or perform other actions
    return HttpResponseRedirect(reverse('login'))


def cancel_plan(request,user_id):
    user = get_object_or_404(Users, id=user_id)
    user.memberShip = 'F'  # Assuming the membership field is called 'memberShip'
    user.save()
    # Redirect to a success page or perform other actions
    return HttpResponseRedirect(reverse('login'))

def registration_cancel(request):
    # Handle the canceled payment and notify the user
    return HttpResponse("Payment canceled.")



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
                        form = LoginForm()
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
                    form = LoginForm()
                    response = HttpResponseRedirect(reverse("student-home"))
                    return response
                else:
                    # render tutor view
                    return HttpResponseRedirect(reverse('tutor-home'))
                  
            else:
                 form = LoginForm()
        else:
            form = LoginForm()

    return render(request, 'login.html', {'form': form})


def getmaterial(request, course_id):
    material = Material.objects.filter(course_id=course_id)
    return render(request, 'getcourses.html', {'material':material})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def grade_view(request,course_id,assignment_id):
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
