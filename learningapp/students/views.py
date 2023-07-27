from django.shortcuts import render, get_object_or_404
from static.forms import addSubmissionForm
from learningapp.models import Course, Material, Assignment, Users, StudentCourses, AssignmentAnswer, Quiz, Question, Option, Result
from learningapp.templates.static.forms import uploadAnswerForm
from django.contrib.auth.decorators import login_required,  user_passes_test
from learningapp.utils import is_student
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from datetime import date,datetime

import json

def get_greeting_message(current_hour):
    if 5 <= current_hour < 12:
        return 'Good Morning!'
    elif 12 <= current_hour < 17:
        return 'Good Afternoon!'
    else:
        return 'Good Evening!'

def get_m(m):
    print(m)
    if m=="S":
        return 'EnlightLearn Silver Plan'
    elif m=="P":
        return 'EnlightLearn Platinum Plan'
    elif m=="G":
        return 'EnlightLearn Gold Plan'
    else:
        return 'EnlightLearn Free Plan'


@login_required
@user_passes_test(is_student)
def home_student(request):
    user = request.session['user']
    student = get_object_or_404(Users,pk=user['id'])
 
    # Get the count of enrolled courses for the student
    enrolled_courses_count = student.enrolled_courses.count()
    # Get the greeting message based on the current time
    current_hour = datetime.now().hour
    greeting_message = get_greeting_message(current_hour)
    # Get the count of assignments that are due but not submitted for the student
    assignments_due_count = Assignment.objects.filter(course_id__students=student, due_date__lte=date.today(), is_submitted=False).count()
    print(user)
    user['membership'] = get_m(student.memberShip)
    return render(request, './students/home.html',{ 'greeting_message': greeting_message,'user':user,'enrolled_courses':enrolled_courses_count,'assignment_due_counts':assignments_due_count} )

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

def view_course_details(request, course_id):
    print("Course_id",course_id)
    course_details = Course.objects.get(id=course_id)
    return render(request, "students/course_detail.html",{'course_details':course_details})

def assignment_submission(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

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
            # form1.assignment.user = user
            # form1.assignment.is_submitted = True
            # form1.assignment.course_id = assignment.course_id
            form1.student = user
            form1.course = assignment.course_id

            form1.save()
            return HttpResponse('successfull')
    else:
        form = addSubmissionForm()

    # if AssignmentAnswer.objects.filter(assignment=assignment, student=request.user).exists():
    #     submission = AssignmentAnswer.objects.get(assignment=assignment, student=request.user)

    return render(request, "students/assignment_submission.html", {'course_details': assignment.course_id,'assignment': assignment,'form': form})


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
    return  render(request, "students/view_assignment.html",{'course_details':course_details,'course_assignments':assignments})

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

    return render(request, './students/courselist.html', {'enrolled_courses':course})

def enrollCourse(request,course_id):
    user = request.session['user']
    i_user = get_object_or_404(Users,pk=user['id'])
    course = get_object_or_404(Course,pk=course_id)
    is_enrolled = StudentCourses.objects.filter(user=i_user, course=course).exists()

    print(is_enrolled)
    if not is_enrolled:
        print(i_user.memberShip)
        total_enrolled_courses = len(StudentCourses.objects.filter(user=i_user))
        if((i_user.memberShip =='F' and total_enrolled_courses ==0 ) or  (i_user.memberShip =='S' and total_enrolled_courses <=3) or (i_user.memberShip =='G' and total_enrolled_courses <=5 ) or (i_user.memberShip =='P')):
            StudentCourses.objects.create(user=i_user, course=course)
            course.students.add(i_user)
            course.save()
        else:
            print('Please upgrade your membership in order to enroll this course.')
    else:
        pass #already enrolled

    return HttpResponseRedirect(reverse('student-courses'))

def view_materials(request, course_id):
    material_details = Material.objects.filter(course_id_id=course_id)
    course_details = Course.objects.get(id=course_id)
    return render(request, "students/view_material.html",{'course_details':course_details,'course_materials':material_details})


def show_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    course_id = quiz.course_id
    obtain_marks = 0
    if request.method == 'POST':
        dictAnswer = request.POST['answer']
        questions = Question.objects.filter(quiz = quiz)
        for question in questions:
            question_id = question.id
            question_marks = question.marks
            answer = Option.objects.filter(question = question, is_correct=True)

            if dictAnswer[question_id] == answer:
                obtain_marks += question_marks
        result = Result()
        result.type = "quiz"
        usr = request.session['user']
        result.user = get_object_or_404(Users,pk=usr['id'])
        result.related_id = quiz_id
        result.grade = obtain_marks
        result.total_grade = quiz.total_marks
        result.save()

    else:
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

        for question in Question.objects.filter(quiz=quiz):
            oQuestion = {}
            oQuestion["question_text"] = question.question_text
            oQuestion["marks"] = question.marks
            lstOptions = []
            oQuestion["lstOptions"] = lstOptions

            print(f"  Question: {question.question_text}")
            print(f"  Marks: {question.marks}")
            print("  Options:")

            for option in Option.objects.filter(question=question):
                oOption = {}
                oOption["option_text"] = option.option_text
                oOption["is_correct"] = option.is_correct
                lstOptions.append(oOption)
                print(f"   option - {option.option_text}")

            lstQuestion.append(oQuestion)

        json_string = json.dumps(oQuiz)
        return render(request, 'students/showquiz.html',
                      {'oQuiz': json_string, 'bAdd': 1, 'quiz_id': quiz_id, 'course_id': course_id})