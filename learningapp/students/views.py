from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from learningapp.models import Course, Material, Assignment, Users, AssignmentAnswer
from learningapp.templates.static.forms import uploadAnswerForm, addMaterialForm
from static.forms import addSubmissionForm
from learningapp.models import Course, Material, Assignment, Users, StudentCourses
from learningapp.templates.static.forms import CreateCourseForm, UpdateCourseForm, addMaterialForm, \
    addAssignmentForm, uploadAnswerForm
from django.contrib.auth.decorators import login_required,  user_passes_test
from learningapp.utils import is_student
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

@login_required
@user_passes_test(is_student)
def home_student(request):
    user = request.session['user']
    return render(request, './students/home.html',{'user':user} )

@login_required
@user_passes_test(is_student)
def getallcourse(request):
    courses = Course.objects.all()
    return render(request, './students/courselist.html', {'courses': courses})


def uploadAnswer(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    print("session")

    if request.method == 'POST':
        form = uploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Updated Successfully")
        return HttpResponse("form is not valid")
    else:
        assignment.document = ''
        form = uploadAnswerForm()
        return render(request, './tutors/addmaterial.html', {'form': form})

def assignment_submission(request):
    assignment = get_object_or_404(Assignment, id=1)
    user_id = None
    if 'user' in request.session:
        data = request.session['user']
        user_id = data['id']
    else:
        print("Not here")

    user = get_object_or_404(Users, pk=user_id)

    if request.method == "POST":
        form = addSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.assignment = assignment
            form1.student = user
            form1.save()
            return HttpResponse('successfull')
    else:
        form = addSubmissionForm()

    # if AssignmentAnswer.objects.filter(assignment=assignment, student=request.user).exists():
    #     submission = AssignmentAnswer.objects.get(assignment=assignment, student=request.user)

    return render(request, "students/assignment_submission.html", {'assignment': assignment,'form': form})


# def addMaterial(request,course_id):
#     if request.method == "POST":
#         form = uploadAnswerForm(request.POST, request.FILES)
#         if form.is_valid():
#             form1 = form.save(commit=False)
#             course_details = Course.objects.get(id=course_id)
#             form1.course_id = course_details
#             form1.save()
#             return HttpResponseRedirect(reverse('tutor-view-course-material',args=[course_id]))
#     else:
#         form = uploadAnswerForm()
#     return render(request, "students/assignment_submission.html", {'form': form})


def viewCourseAssignments(request,course_id):
    course_details = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course_id=course_id)
    return HttpResponse('Successfully')
    # return render(request, "tutors/courseAssignments.html",{'course_details':course_details,'course_assignments':assignments})
def getQuizesByCourseId(request, course_id):
    course = get_object_or_404(Course, pk=course_id)


@login_required
@user_passes_test(is_student)
def getAvailableCourses(request):
    user = request.session['user']
    courses= Course.objects.exclude(students__id=user['id'])
    return render(request, './students/browseCourses.html', {'available_courses':courses})

@login_required
@user_passes_test(is_student)
def getEnrolledCourses(request):
    user = request.session['user']
    course = Course.objects.filter(students__id=user['id'])
    print(course[0].tutor.username)
    return render(request, './students/courselist.html', {'enrolled_courses':course})

def enrollCourse(request,course_id):
    user = request.session['user']
    i_user = get_object_or_404(Users,pk=user['id'])
    course = get_object_or_404(Course,pk=course_id)
    # Check if the student is already enrolled in the course
    is_enrolled = StudentCourses.objects.filter(user=i_user, course=course).exists()

    print(is_enrolled)
    if not is_enrolled:
        print(i_user.memberShip)
        total_enrolled_courses = len(StudentCourses.objects.filter(user=i_user))
        if((i_user.memberShip =='F' and total_enrolled_courses ==0 ) or  (i_user.memberShip =='S' and total_enrolled_courses ==3) or (i_user.memberShip =='G' and total_enrolled_courses ==5 ) or (i_user.memberShip =='P')):
            StudentCourses.objects.create(user=i_user, course=course)
            course.students.add(i_user)
            course.save()
        else:
            print('Please upgrade your membership in order to enroll this course.')
    else:
        pass #already enrolled

    return HttpResponseRedirect(reverse('student-courses'))