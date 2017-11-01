from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from pprint import pprint
from .models import User
import json
# Create your views here.
@csrf_exempt
def create(request):
    if (request.method == "POST"):
        user = json.loads(request.body)
        user_name = user['nickname']
        user_pass = user['password']
        user_phone = user['phone']
        user = User()
        user.nickname = user_name
        user.password = user_pass
        user.phone = user_phone
        user.set_password(user.password)
        user.save()
        user = {
            'success':1,
            'username': user_name
        }
        return HttpResponse(json.dumps(user))