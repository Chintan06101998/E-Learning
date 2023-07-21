# learningapp/utils.py
from learningapp.models import  Users

def is_tutor(user):
    c_user = Users.objects.get(username=user)
    print(c_user.user_type)
    return user.is_authenticated and int(c_user.user_type) == 1

def is_student(user):
    c_user = Users.objects.get(username=user)
    return user.is_authenticated and int(c_user.user_type) == 0
