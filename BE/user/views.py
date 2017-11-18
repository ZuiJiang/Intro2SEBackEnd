from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import JsonResponse
from pprint import pprint
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.validators import validate_email
from .utlis.MyEmail import send_your_email
import json
from .models import Profile
from .models import Email
# Create your views here.
@csrf_exempt
def register(request):
    if (request.method == "POST"):
        user_data = json.loads(request.body)
        user_name = user_data['username']
        user_pass = user_data['password']
        user_email = user_data['email']
        user_validate = user_data['validate']
        try:
            email = Email.objects.get(email = user_email)
        except:
            return_msg = {
                "success": 0,
                "err_msg": "请确定邮箱是否正确"
            }
            return JsonResponse(return_msg)
        validate = model_to_dict(email)['validate']
        if(user_validate == validate):
            #validate is right
            try:
                #check if exist the user 
                user = User.objects.get(username = user_name)
                return_msg = {
                    "success": 0,
                    "err_msg": "用户名重复"
                }
                return JsonResponse(return_msg)
            except:
                #register success
                try:
                    user = User.objects.create_user(user_name, user_email, user_pass) 
                    Profile.objects.create(user=user, finishNum=0)
                    return_msg = {
                        "success":1
                    }
                except:
                    return_msg = {
                        "success": 0,
                        "err_msg": "用户名仅能含有不能含有?,!等特殊字符"
                    }
        else:
            return_msg = {
                "success": 0,
                "err_msg": "错误的验证码"
            }
        return JsonResponse(return_msg)
    elif(request.method == "GET"):
        if(request.GET.get("username")):
            user_name = request.GET.get("username")
            try:
                user = User.objects.get(username = user_name)
                return_msg = {
                    "success": 0,
                    "err_msg": "用户名重复"
                } 
            except:
                # if need check the email
                if(request.GET.get("email")):
                    user_email = request.GET.get("email")
                    try:
                        user = User.objects.get(email = user_email)
                        return_msg = {
                            "success": 0,
                            "err_msg": "邮箱重复"
                        } 
                    except:
                        return_msg = {
                            "success": 1, 
                            }
                else:
                    return_msg = {
                        "success": 1,
                    }
            return JsonResponse(return_msg)
        elif(request.GET.get("email")):
            user_email = request.GET.get("email")
            try:
                user = User.objects.get(email = user_email)
                return_msg = {
                    "success": 0,
                    "err_msg": "邮箱重复"
                }
            except:
                return_msg = {
                    "success": 1
                }
            return JsonResponse(return_msg)

#user login
@csrf_exempt
def login(request):
    if(request.method == "POST"):
        user_msg = json.loads(request.body)
        if('username' in user_msg):
            user_name = user_msg['username']
        elif ('email' in user_msg):
            email = user_msg['email']
            try:
                validate_email(email)
            except:
                return_msg = {
                    "success": 0,
                    "err_msg": "请确保邮箱格式"
                }
                return JsonResponse(return_msg)
            try:
                user_Model = User.objects.get(email=email)
                user_name = model_to_dict(user_Model)['username']
            except:
                return_msg = {
                    "success": 0,
                    "err_msg": "Email doesn't exists"
                }
                return JsonResponse(return_msg)
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
        return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg":"Check the method"
        }
        return JsonResponse(return_msg)

@csrf_exempt
def sendEmail(request):
    if(request.method == "POST"):
        user_email = (json.loads(request.body))['email']
        try:
            validate_email(user_email)
        except:
            return_msg = {
                "success": 0,
                "err_msg": "请确保邮箱正确"
            } 
            return JsonResponse(return_msg)
        validate = send_your_email(user_email)
        print(validate)
        try:
            # if the email exists then update the validate
            exist_email = Email.objects.get(email = user_email)
            exist_email.validate = validate
            exist_email.save()
        except:
            # if the email doesn't exist then create the email 
            Email.objects.create(email = user_email, validate = validate)
        return_msg = {
            "success": 1,
        }
        return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg": "请确保请求方法正确"
        }
        return JsonResponse(return_msg)

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
        return JsonResponse(return_msg)
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
            return JsonResponse(return_msg) 
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
            return JsonResponse(return_msg)
        else:
            return_msg = {
                "success": 0,
                "err_msg": "错误的验证码"
            }
        return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg":"确保方法正确"
        }
        return JsonResponse(return_msg)
