from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from learningapp.models import Course, Material, Assignment, Users
from learningapp.templates.static.forms import CreateCourseForm, UpdateCourseForm, addMaterialForm, \
    addAssignmentForm, uploadAnswerForm


def getallcourse(request):
    courses = Course.objects.all()
    return render(request, './students/courselist.html', {'courses': courses})


def uploadAnswer(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':
        form = uploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Updated Successfully")

    else:
        assignment.document = ''
        form = uploadAnswerForm()
        return render(request, './tutors/addmaterial.html', {'form': form})

def getQuizesByCourseId(request, course_id):
    course = get_object_or_404(Course, pk=course_id)