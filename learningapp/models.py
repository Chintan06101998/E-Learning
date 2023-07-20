from django.db import models
from django.contrib.auth.models import AbstractUser, User
import datetime
import json


from django.db.models import JSONField


class Users(User):
    MEMBERSHIP_CHOICE = [
        ('F', 'Free'),
        ('S', 'Silver'),
        ('G', 'Gold'),
        ('P', 'Premium')]

    USER_TYPE = (
        ('0', 'Student'),
        ('1', 'Professor')
    )

    user_type = models.CharField(max_length=255, choices=USER_TYPE, null=True, default='0')
    memberShip = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICE, default='F')

    def __str__(self):
        return self.username



class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    #enrolled_student = models.OneToOneField(Users, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='courses_tutored')
    students = models.ManyToManyField(Users, related_name='enrolled_courses') #adding when student when register
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
    quiz_data_json = models.TextField()


class Results(models.Model):
    TYPE = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment')
    ]
    related_id = models.CharField(max_length=255)
    user_id = models.OneToOneField(Users, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE, default='assignment')
    grade = models.PositiveIntegerField(default=0)



class AssignmentAnswer(models.Model):
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    answer = models.FileField(upload_to='course_materials/documents', null=True)
    submission_date = models.DateField(null=True, auto_now=True)
    submission_time = models.TimeField(null=True, auto_now=True)

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





