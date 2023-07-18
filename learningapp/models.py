from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

from django.db.models import JSONField


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    is_student = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name


# class User(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('student', 'Student'),
#         ('tutor', 'Tutor'),
#     )
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    #enrolled_student = models.OneToOneField(Users, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Users, related_name='enrolled_courses', blank=True, null=False) #adding when student when register
    createdAt = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    material_name = models.CharField(max_length=255)
    material_disc = models.CharField(max_length=255)
    document = models.FileField(upload_to='course_materials/documents',null=True)
    #assignment = models.FileField(upload_to='course_materials/assignments')
    #end_date = models.DateField()
    #aaignment_grade = models.IntegerField()

    def __str__(self):
        return  self.material_name

class Assignment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    document = models.FileField(upload_to='course_materials/documents', null=True)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(null=True)
    grade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return  self.assignment_name



class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)
    description = models.TextField()
    # questions = JSONField()
    quiz_start_date = models.DateTimeField()
    quiz_due_date = models.DateTimeField()
    marks = models.IntegerField(default=0)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()


class Option(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class Results(models.Model):
    TYPE = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment')
    ]
    id = models.AutoField(primary_key=True)
    related_id = models.CharField(max_length=255)
    user_id = models.OneToOneField(Users, on_delete=models.CASCADE)
    # type = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    quiz_grade = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    assignment_grade = models.OneToOneField(Material, on_delete=models.CASCADE)


class MaterialAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    material_id = models.OneToOneField(Material, on_delete=models.CASCADE)
    student_id = models.OneToOneField(Users, on_delete=models.CASCADE)
    answers = models.CharField(max_length=255)
    submission_date = models.DateField()


class Subscription(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('none', 'None'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='subscription')
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES)


class Grade(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    course_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
