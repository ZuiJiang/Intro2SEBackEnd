from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from pprint import pprint
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .utlis.MyEmail import send_your_email
import json
from .models import Profile
from .models import Email
# Create your views here.
@csrf_exempt
def register(request):
    if (request.method == "POST"):
        user = json.loads(request.body)
        user_name = user['username']
        user_pass = user['password']
        user_email = user['email']
        user_validate = user['validate']
        try:
            email = Email.objects.get(email = user_email)
        except:
            return_msg = {
                "success": 0,
                "err_msg": "请确定邮箱是否正确"
            }
            return HttpResponse(json.dumps(return_msg)) 
        validate = model_to_dict(email)['validate']
        if(user_validate == validate):
            #register success
            try:
                user = User.objects.get(username = user_name)
                return_msg = {
                    "success": 1,
                    "err_msg": "用户名重复"
                }
                return HttpResponse(json.dumps(return_msg))
            except:
                User.objects.create_user(user_name,user_email,user_pass) 
                return_msg = {
                    "success":1
                }
        else:
            return_msg = {
                "success": 0,
                "err_msg": "错误的验证码"
            }
        return HttpResponse(json.dumps(return_msg))

@csrf_exempt
def login(request):
    if(request.method == "POST"):
        user_msg = json.loads(request.body)
        if('username' in user_msg):
            user_name = user_msg['username']
        elif ('email' in user_msg):
            email = user_msg['email']
            try:
                user_Model = User.objects.get(email=email)
                user_name = model_to_dict(user_Model)['name']
            except:
                return_msg = {
                    "success": 0,
                    "err_msg": "Email doesn't exists"
                }
                return HttpResponse(json.dumps(return_msg))
        user_password = user_msg['password']
        user = authenticate(username=user_name, password=user_password)
        if user is not None:
            auth_login(request, user)
            return_msg = {
                "success": 1,
                "username": user_name
            }
        else:
            return_msg = {
                "success": 0,
                "err_msg": "Confirm Password"
            }
        return HttpResponse(json.dumps(return_msg))
    else:
        return_msg = {
            "success": 0,
            "err_msg":"Check the method"
        }
        return HttpResponse(json.dumps(return_msg))
@csrf_exempt
def sendEmail(request):
    if(request.method == "POST"):
        user_email = json.loads(request.body)['email']
        validate = send_your_email(user_email)
        try:
            exist_email = Email.objects.get(email = user_email)
            exist_email.validate = validate
            exist_email.save()
        except:
            Email.objects.create(email = user_email, validate = validate)
        return_msg = {
            "success": 1,
        }
        return HttpResponse(json.dumps(return_msg))
    else:
        return_msg = {
            "success": 0,
            "err_msg": "请确保请求方法正确"
        }
        return HttpResponse(json.dumps(return_msg))

@csrf_exempt
def password(request):
    #change the password
    if(request.method == "POST"):  
        user_data = json.loads(request.body)
        user_username = user_data['username']
        user_oldPass = user_data['oldPassword']
        user_newPass = user_data['newPassword']
        user = authenticate(username=user_username, password=user_oldPass)
        if(user is not None):
            u = User.objects.get(username = user_username)
            u.set_password(user_newPass)
            u.save()
            return_msg = {
                "success": 1,
            }
        else:
            return_msg = {
                "success": 0,
                "err_msg": "请保证密码正确"
            }
        return HttpResponse(json.dumps(return_msg))
    #fucking the user forget password
    if(request.method == "PUT"):
        user_data = json.loads(request.body)
        user_username = user_data['username']
        user_email = user_data['email']
        user_validate = user_data['validate']
        user_newPass = user_data['newPassword']
        try:
            email = Email.objects.get(email = user_email)
        except:
            return_msg = {
                "success": 0,
                "err_msg": "请确定邮箱是否正确"
            }
            return HttpResponse(json.dumps(return_msg)) 
        validate = model_to_dict(email)['validate']
        if(user_validate == validate):
            #confirm user
            try:
                user = User.objects.get(username = user_name)
                user.set_password(user_newPass)
                user.save()
                return_msg = {
                    "success": 1,
                }
            except:
                return_msg = {
                    "success":0,
                    "err_msg":"查无此人"
                }
            return HttpResponse(json.loads(return_msg))
        else:
            return_msg = {
                "success": 0,
                "err_msg": "错误的验证码"
            }
        return HttpResponse(json.dumps(return_msg))
    else:
        return_msg = {
            "success": 0,
            "err_msg":"确保方法正确"
        }
        return HttpResponse(json.dumps(return_msg))