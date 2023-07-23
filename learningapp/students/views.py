from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from learningapp.models import Course, Material, Assignment, Users, AssignmentAnswer
from learningapp.templates.static.forms import uploadAnswerForm, addMaterialForm
from static.forms import addSubmissionForm


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