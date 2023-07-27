from learningapp.models import Users
from django.shortcuts import get_object_or_404

def is_tutor(user):
    c_user = get_object_or_404(Users, username=user)
    print(c_user.user_type)
    return user.is_authenticated and int(c_user.user_type) == 1


def is_student(user):
    c_user = get_object_or_404(Users, username=user)
    return user.is_authenticated and int(c_user.user_type) == 0
