import json
from django.urls import reverse
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from learningapp.models import Course, Material, Assignment, Quiz
from learningapp.templates.static.forms import CreateCourseForm, UpdateCourseForm, addMaterialForm, \
    addAssignmentForm, addMarksForms
from learningapp.utils import is_tutor

@login_required
@user_passes_test(is_tutor)
def createCourse(request):
    if request.method == "POST":
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form1 = form.save(commit=False)
            user = request.session['user']
            form1.tutor_id = user['id']
            form1.save()
            return HttpResponseRedirect(reverse('tutor-courses'))
    else:
        form = CreateCourseForm()
    return render(request, "tutors/coursecreate.html", {'form': form})

@login_required
@user_passes_test(is_tutor)
def viewCourse(request,course_id):
    course_details = Course.objects.get(id=course_id)
    enrolled_students = course_details.students.all()
    return render(request, "tutors/viewcourse.html",{'course_details':course_details,"enrolled_students":enrolled_students})

@login_required
@user_passes_test(is_tutor)
def viewCourseMaterials(request,course_id):
    course_details = Course.objects.get(id=course_id)
    material_details = Material.objects.filter(course_id=course_id)
    return render(request, "tutors/courseMaterial.html",{'course_details':course_details,'course_materials':material_details})


@login_required
@user_passes_test(is_tutor)
def viewCourseAssignments(request,course_id):
    course_details = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course_id=course_id)
    return render(request, "tutors/courseAssignments.html",{'course_details':course_details,'course_assignments':assignments})


@login_required
@user_passes_test(is_tutor)
def viewCourseQuizzes(request,course_id): 
    course_details = Course.objects.get(id=course_id)
    quizzes =[]
    return render(request, "tutors/viewcourse.html",{'course_details':course_details,"course_quizzes":quizzes})

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

@login_required
@user_passes_test(is_tutor)
def home_tutor(request):
    user = request.session['user']
    return render(request, 'tutors/home.html',{'user':user} )

@login_required
@user_passes_test(is_tutor)
def addMaterial(request,course_id):
    if request.method == "POST":
        form = addMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            course_details = Course.objects.get(id=course_id)
            form1.course_id = course_details
            form1.save()
            return HttpResponseRedirect(reverse('tutor-view-course-material',args=[course_id]))
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
@login_required
@user_passes_test(is_tutor)
def addAssignment(request,course_id):
    if request.method == "POST":
        form = addAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            course_details = Course.objects.get(id=course_id)
            form1.course_id = course_details
            form1.save()
            return HttpResponseRedirect(reverse('tutor-view-course-assignments',args=[course_id]))
        else:
            print(form.add_error())
    else:
        form = addAssignmentForm()
    return render(request, "tutors/createAssignment.html", {'form': form})


def updateAssignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == "POST":
        form = addAssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return HttpResponse(
                'Assignment updated Successfully')  # Replace 'material_list' with the URL name of your material list view.
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

@login_required
@user_passes_test(is_tutor)
def getcourse(request):
    user = request.session['user']
    if user['usertype'] == '1':
        courses = Course.objects.filter(tutor_id=user['id'])
        return render(request,'tutors/courses.html',{'courses':courses})


def addMarks(request):
    if request.method == "POST":
        form = addMarksForms(request.POST)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return render(request, "tutors/addMarks.html", {'form': form1})
    else:
        form = addMarksForms()
    return render(request, "tutors/addMarks.html", {'form': form})

def createquiz(request):
    quiz_data = [
        {
            'question': 'What is Django?',
            'option1': 'A programming language',
            'option2': 'A web framework',
            'option3': 'A database management system',
            'option4': 'An operating system',
            'answer': 'A web framework',
        },
        {
            'question': 'What is Python?',
            'option1': 'A markup language',
            'option2': 'A web framework',
            'option3': 'A programming language',
            'option4': 'An operating system',
            'answer': 'A programming language',
        },
        # Add more quizzes here...
    ]

    # Convert the list to a JSON string
    quiz_data_json = json.dumps(quiz_data)

    # Save the JSON string in the database
    quiz_model = Quiz.objects.create(quiz_data_json=quiz_data_json)

    return HttpResponse('Success')



def updateQuiz(request, quiz_id):
    quiz = get_object_or_404(pk=quiz_id)

    # Updated quiz data
    updated_data = {
        'question': 'What is Django?',
        'option1': 'A powerful web framework',
        'option2': 'A web design tool',
        'option3': 'A database management system',
        'option4': 'An operating system',
        'answer': 'A powerful web framework',
    }

    # Set the updated quiz data
    quiz.set_quiz_data(updated_data)

    # Save the quiz object with updated data
    quiz.save()

    return HttpResponse("Quiz Updated Successfully")
