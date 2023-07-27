import json
from datetime import timedelta

from django.urls import reverse
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from learningapp.models import Course, ClassMaterial, Assignment, AssignmentAnswer, Question, Option, Quiz
from learningapp.templates.static.forms import CreateCourseForm, UpdateCourseForm, addMaterialForm, \
    addAssignmentForm, addMarksForms, AddQuizForm, QuestionFormSet, UpdateQuizForm

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
        form = CreateCourseForm(initial={'name':'','description':''})
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
    material_details = ClassMaterial.objects.filter(course_id=course_id)
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
    quizzes = Quiz.objects.filter(course = course_details)
    print(quizzes)
    return render(request, "tutors/viewquiz.html",{'course_details':course_details,"course_quizzes":quizzes})

def updateCourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        form = UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tutor-courses'))
    else:
        form = UpdateCourseForm(instance=course)

    return render(request, "tutors/coursecreate.html", {'form': form})

@login_required
@user_passes_test(is_tutor)
def deleteCourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        course.delete()
        return HttpResponseRedirect(reverse('tutor-courses'))

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
        form = addMaterialForm(initial={'name':'','description':''})
    return render(request, "tutors/addmaterial.html", {'form': form})


@login_required
@user_passes_test(is_tutor)
def updateMaterial(request, material_id):
    material = get_object_or_404(ClassMaterial, pk=material_id)
    fakepath=''
    if request.method == "POST":
        form = addMaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tutor-view-course-material',args=[material.course_id.id]))
    else:
        form = addMaterialForm(instance=material)
        patharr= material.document.name.split('/')
        fakepath = '/fakepath/'+patharr[len(patharr)-1]

    return render(request, "tutors/addmaterial.html", {'form': form, 'material_id': material_id,'fakepath':fakepath})

@login_required
@user_passes_test(is_tutor)
def deleteMaterial(request, material_id):
    material = get_object_or_404(ClassMaterial, pk=material_id)

    if request.method == "POST":
        material.delete()
        return HttpResponseRedirect(reverse('tutor-view-course-material',args=[material.course_id.id]))

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
        form = addAssignmentForm(initial={'name':'','description':'','initial_due_time':'','initial_due_date':''})
    return render(request, "tutors/createAssignment.html", {'form': form})


@login_required
@user_passes_test(is_tutor)
def updateAssignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    initial_due_time=''
    initial_due_date=''
    if request.method == "POST":
        form = addAssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tutor-view-course-assignments',args=[assignment.course_id.id])) 
    else:
        form = addAssignmentForm(instance=assignment)
        patharr= assignment.document.name.split('/')
        fakepath = '/fakepath/'+patharr[len(patharr)-1]
        initial_due_time = assignment.due_time.strftime('%H:%M')
        initial_due_date= assignment.due_date.strftime('%Y-%m-%d')
    return render(request, "tutors/createAssignment.html", {'form': form, 'assignment_id': assignment_id,'fakepath':fakepath, 'initial_due_time':initial_due_time,'initial_due_date':initial_due_date})

@login_required
@user_passes_test(is_tutor)
def deleteAssignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == "POST":
        assignment.delete()
        return HttpResponseRedirect(reverse('tutor-view-course-assignments',args=[assignment.course_id.id])) 
    return render(request, "tutors/materialdelete.html", {'assignment': assignment})

@login_required
@user_passes_test(is_tutor)
def getcourse(request):
    user = request.session['user']
    if user['usertype'] == '1':
        courses = Course.objects.filter(tutor_id=user['id'])
        courseses = Course.objects.filter(pk=1)
        # students  = courseses.students.all()
        print("---->")
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


def parse_quiz_data(post_data):
    quiz_data = {}
    quiz_data['quiz_name'] = post_data.get('quiz_name')
    quiz_data['duration'] = post_data.get('duration')

    questions = []
    option_keys = [k.split('-')[1] for k, v in post_data.items() if k.startswith('q-option')]
    option_keys1 = {k.split('-')[-1]:k.split('-')[1] for k, v in post_data.items() if k.startswith('q-option')}
    # print(option_keys1)
    # print(option_keys)
    num_questions = len([k for k in option_keys1.values()])

    for i in range(1, num_questions + 1):
        question = {}
        # print("========>Question number : ", i,"<=========")
        question['question'] = post_data.get(f'q-question-{i}')
        question['options'] = []
        for j in range(1,5):
            option = post_data.get(f'q-option{j}-{i}')
            # print("My oprion ===> ", option, "key option", j, "-",i)
            question['options'].append(option)

        question['answer'] = post_data.get(f'q-answer-{i}')
        question['marks'] = post_data.get(f'q-marks-{i}')
        questions.append(question)

    quiz_data['questions'] = questions

    return quiz_data

def add_quiz(request,course_id):
    if request.method == 'POST':
        quiz_data = parse_quiz_data(request.POST)
        totalMarks = 0
        course = get_object_or_404(Course, pk = course_id)
        quiz = Quiz()
        quiz.course = course
        quiz.quiz_name = quiz_data['quiz_name']
        quiz.total_marks = totalMarks
        duration_str = quiz_data['duration']
        duration_timedelta = timedelta(hours=int(duration_str[:2]), minutes=int(duration_str[3:5]),
                                       seconds=int(duration_str[6:]))
        quiz.duration = duration_timedelta
        quiz.save()

        for que in quiz_data['questions']:
            ques = Question()
            ques.question_text = que["question"]
            answer_no = que["answer"][-1:]
            ques.marks = que["marks"]
            ques.quiz = quiz
            totalMarks = totalMarks + int(ques.marks)
            ques.save()
            count = 1
            # print("-----> :",que["options"])
            for opt in que["options"]:
                opts = Option()
                opts.option_text = opt
                opts.question = ques
                if count == answer_no:
                    opts.is_correct = True
                count = count + 1
                opts.save()

        quiz.total_marks = totalMarks
        quiz.save()
        print(quiz.id)
        return HttpResponseRedirect(
            reverse('tutor-view-course-quizzes', args=[course_id]))  # Redirect to the course list page after deletion

    else:
        form = AddQuizForm()

    oQuiz = {}
    oQuiz['bAdd'] = True
    json_string = json.dumps(oQuiz)
    return render(request, 'tutors/add_quiz.html', {'quiz_form': form,'oQuiz':json_string,'bAdd':0, 'course_id':course_id})


def update_quiz(request,quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    course_id = quiz.course.id

    if request.method == 'POST':
        print("Post")
        quiz_data = parse_quiz_data(request.POST)
        print("Update :---> ")
        print(quiz_data)
        totalMarks = 0
        quiz.quiz_name = quiz_data['quiz_name']
        quiz.total_marks = totalMarks
        duration_str = quiz_data['duration']
        duration_timedelta = timedelta(hours=int(duration_str[:2]), minutes=int(duration_str[3:5]),
                                       seconds=int(duration_str[6:]))
        quiz.duration = duration_timedelta
        quiz.save()
        Question.objects.filter(quiz = quiz).delete();
        for que in quiz_data['questions']:
            ques = Question()
            ques.question_text = que["question"]
            answer_no = que["answer"][-1:]
            ques.marks = que["marks"]
            ques.quiz = quiz
            totalMarks = totalMarks + int(ques.marks)
            ques.save()
            count = 1
            # print("-----> :",que["options"])
            for opt in que["options"]:
                opts = Option()
                opts.option_text = opt
                opts.question = ques
                if count == answer_no:
                    opts.is_correct = True
                count = count + 1
                opts.save()

        quiz.total_marks = totalMarks
        quiz.save()
        return HttpResponseRedirect(
            reverse('tutor-view-course-quizzes', args=[course_id]))  # Redirect to the course list page after deletion
    else:
        print("Get")
        oQuiz = {}
        # Print all the data from the quiz model
        oQuiz["quiz_name"] = quiz.quiz_name
        oQuiz["total_marks"] = quiz.total_marks

        duration_timedelta = quiz.duration
        hours = duration_timedelta.seconds // 3600
        minutes = (duration_timedelta.seconds // 60) % 60
        seconds = duration_timedelta.seconds % 60

        # Convert the extracted values to a string in the "HH:MM:SS" format
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        oQuiz["duration"] = duration_str
        lstQuestion = []
        oQuiz["lstQuestion"] = lstQuestion

        print(f"Total Marks: {quiz.total_marks}")
        print(f"Duration: {quiz.duration}")
        print("Questions:")

        for question in Question.objects.filter(quiz = quiz):
            oQuestion = {}
            oQuestion["question_text"] = question.question_text
            oQuestion["marks"] = question.marks
            lstOptions = []
            oQuestion["lstOptions"] = lstOptions

            print(f"  Question: {question.question_text}")
            print(f"  Marks: {question.marks}")
            print("  Options:")

            for option in Option.objects.filter(question = question):
                oOption = {}
                oOption["option_text"] = option.option_text
                oOption["is_correct"] = option.is_correct
                lstOptions.append(oOption)
                print(f"   option - {option.option_text}")

            lstQuestion.append(oQuestion)

        form = AddQuizForm(quiz)
        json_string = json.dumps(oQuiz)
        return  render(request, 'tutors/add_quiz.html', {'quiz_form': form,'oQuiz':json_string,'bAdd':1,'quiz_id':quiz_id,'course_id':course_id})

def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    print(quiz)
    if request.method == "POST":
        quiz.delete()
        return HttpResponseRedirect(reverse('tutor-view-course-quizzes', args=[quiz.course.id]))   # Redirect to the course list page after deletion

# def getAssignment(request, course_id):
    # assignments = Assignment.objects.filter(course_id_id=course_id)
    # AssignmentAnswer.objects.filter(assignment_id=)


def assignment_grade(request,course_id):
    data = {}
    lstAssignData = []
    data['lstAssignment'] = lstAssignData
    assignmentList = Assignment.objects.filter(course_id_id=course_id)
    print("Assignment Grade",str(len(assignmentList)))
    for assign in assignmentList:
        AssignData = {}
        lstSubData= []
        AssignData['assign_name'] = assign.name
        AssignData['lstSubData'] = lstSubData


        lstAssignData.append(AssignData)
        assignment_answer = AssignmentAnswer.objects.filter(assignment_id=assign.id)
        for sub in assignment_answer:
            submission_data = {}
            lstSubData.append(submission_data)
            data[assign.id] = submission_data

            submission_data['StudentName'] = sub.student.username
            submission_data['Document'] = sub.document
            submission_data['TotalMarks'] = sub.assignment.grade
    print(data)
    if request.method == "POST":
        form = addMarksForms(request.POST)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return HttpResponse("marks given")
    else:
        form = addMarksForms()
    return render(request, "tutors/grade_view.html", {'form': form, 'data':data})



