from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from learningapp.models import Course, Material, Assignment, Users
from learningapp.templates.static.forms import  CreateCourseForm, UpdateCourseForm, addMaterialForm, \
    addAssignmentForm


def createCourse(request):
    if request.method == "POST":
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()

            return render(request, "tutors/coursecreate.html", {'form': form1})
    else:
        form = CreateCourseForm()
    return render(request, "tutors/coursecreate.html", {'form': form})


def updateCourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        form = UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return HttpResponse('course_detail')
    else:
        form = UpdateCourseForm(instance=course)

    return render(request, "tutors/courseupdate.html", {'form': form})


def deleteCourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        course.delete()
        return HttpResponse('course_list')  # Redirect to the course list page after deletion

    return render(request, "tutors/coursedelete.html", {'course': course})


def addMaterial(request):
    if request.method == "POST":
        form = addMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return render(request, "tutors/addmaterial.html", {'form': form1})
    else:
        form = addMaterialForm()
    return render(request, "tutors/addmaterial.html", {'form': form})


def updateMaterial(request, material_id):
    material = get_object_or_404(Material, pk=material_id)
    if request.method == "POST":
        form = addMaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return HttpResponse(
                'material_list')  # Replace 'material_list' with the URL name of your material list view.
    else:
        material.document = ''
        form = addMaterialForm(instance=material)
    return render(request, "tutors/updatematerial.html", {'form': form, 'material_id': material_id})


def deleteMaterial(request, material_id):
    material = get_object_or_404(Material, pk=material_id)

    if request.method == "POST":
        material.delete()
        return HttpResponse('Successfully Delete')  # Redirect to the course list page after deletion

    return render(request, "tutors/materialdelete.html", {'material': material})


# ASSIGNMENT

def addAssignment(request):
    if request.method == "POST":
        form = addAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return render(request, "tutors/addmaterial.html", {'form': form1})
    else:
        form = addAssignmentForm()
    return render(request, "tutors/addmaterial.html", {'form': form})


def updateAssignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == "POST":
        form = addAssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return HttpResponse(
                'Assignment updated Successfully')  #Replace 'material_list' with the URL name of your material list view.
    else:
        assignment.document = ''
        form = addAssignmentForm(instance=assignment)
    return render(request, "tutors/updatematerial.html", {'form': form, 'assignment_id': assignment_id})


def deleteAssignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == "POST":
        assignment.delete()
        return HttpResponse('Successfully Deleted')  # Redirect to the course list page after deletion

    return render(request, "tutors/materialdelete.html", {'assignment': assignment})

def getallCourses(request, prof_id):
    user = Users.objects.filter(is_student=False)
