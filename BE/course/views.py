# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.forms.models import model_to_dict
from pprint import pprint
from .models import Paper
from .models import Problem
from .models import Record
from .models import Ans_Pic
from .models import Pro_Pic
from .models import Option
import json
# Create your views here.

# choose the course
@csrf_exempt
def course(request):
    if (request.method == "GET") :
        if(request.GET.get("course")):
            course_type = request.GET.get("course")
            paper_set = Paper.objects.filter(paper_type=course_type)
            count = 0
            papers = []
            for paper in paper_set:
                paper_dict = model_to_dict(paper)
                paper_dict.pop('problem_num')
                paper_dict.pop('paper_course')
                paper_dict.pop('paper_type')
                papers.append(paper_dict)
                count += 1
            return_dict = {
                "success": 1,
                "num": count,
                "papers": papers
            }
            return HttpResponse(json.dumps(return_dict))
        else:
            return_msg = {
                "success": 0,
                "err_msg": "参数不正确"
            }
            return HttpResponse(json.dumps(return_msg))
    else:
        return_msg = {
            "success": 0,
            "err_msg": "方法不正确"
        }
        return HttpResponse(json.dumps(return_msg)) 

# choose the paper
@csrf_exempt
def paper(request):
    if(request.method == "GET"):
        if(request.GET.get("paperId")):
            paper_id = request.GET.get("paperId")
            problems = Problem.objects.filter(paper = paper_id)
            count = 0
            problem_list = []
            for problem in problems:
                problem_dict = {}
                problem_dict['ProblemId'] = model_to_dict(problem)['id']
                problem_dict['ProblemOrder'] = model_to_dict(problem)['pro_order']
                count += 1
                problem_list.append(problem_dict)
            pprint(problem_list)
            return_dict = {
                "success": 1,
                "ProblemNum": count,
                "Problems":problem_list
            }
            return HttpResponse(json.dumps(return_dict))
        else:
            return_msg = {
                "success": 0,
                "err_msg": "参数不正确"
            }
            return HttpResponse(json.dumps(return_msg))
    else:
        return_msg = {
            "success": 0,
            "err_msg": "方法不正确"
        }
        return HttpResponse(json.dumps(return_msg)) 

#judge the answer
@csrf_exempt
def judge(request):
    if(request.method == "GET"):
        if(request.GET.get("ProblemId") and request.GET.get("ans")):
            ProblemId = request.GET.get("ProblemId")
            ans = request.GET.get("ans")
            return_msg = {
                "success":1
            }
            if(ans == model_to_dict(Problem.objects.get(id = ProblemId))["pro_ans"]):
                return_msg["result"] = 1
            else:
                return_msg["result"] = 0
            return HttpResponse(json.dumps(return_msg))
        else:
            return_msg = {
                "success": 0,
                "err_msg": "确保参数名完整"
            }
            return HttpResponse(json.dumps(return_msg))
    else:
        return_msg = {
            "success": 0,
            "err_msg": "请检查方法"
        }
        return HttpResponse(json.dumps(return_msg))
#choose the problem 
@csrf_exempt
def problem(request):
    if(request.method == "GET"):
        if(request.GET.get("ProblemId")):
            ProblemId = request.GET.get("ProblemId")
            problem = model_to_dict(Problem.objects.get(id = ProblemId))
            problem.pop("paper")
            if(problem["pro_type"] == 1 or problem["pro_type"] == 2):
                option_list = []
                if(problem["pro_type"] == 1):
                    Options = Option.objects.filter(problem__id = ProblemId)
                    for option in Options:
                        option_list.append(model_to_dict(option)['option']) 
                        problem['option'] = option_list
                problem.pop("pro_ans")
            problem['success'] = 1
            return HttpResponse(json.dumps(problem))
        else:
            return_msg = {
                "success" : 0,
                "err_msg" : "参数不正确"
            }
            return HttpResponse(json.dumps(return_msg))
    else:
        return_msg = {
            "success": 0,
            "err_msg": "方法不正确"
        }
        return HttpResponse(json.dumps(return_msg))

#add the problem into the record
@csrf_exempt
def record(request):
    if(request.method == "POST"):
        data = json.loads(request.body)
        pprint(data)
        problemId = data['ProblemId']
        username = data['username']
        note = data['username']
        Record.objects.create(pro_id = problemId, pro_User = username, pro_note = note)
        return_msg = {
            "success":1
        }
        return HttpResponse(json.dumps(return_msg))
    #check the user problem record
    elif(request.method == "GET"):
        if(request.GET.get("username")):
            username = request.GET.get("username")
            records = Record.objects.filter(pro_User = username)
            count = 0
            problem_list = []
            for record in records:
                pro_id = model_to_dict(record)['pro_id']
                pro_note = model_to_dict(record)['pro_note']
                problem = model_to_dict(Problem.objects.get(id = pro_id))
                problem["problemNote"] = pro_note
                 
                problem_list.append(problem)
            return_msg = {
                "problemNum": count,
                "problems": problem_list
            }
    else:
        return_msg = {
            "success": 0,
            "err_msg": "方法不正确"
        }
        return HttpResponse(json.dumps(return_msg))
