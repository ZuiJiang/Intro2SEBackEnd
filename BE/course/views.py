# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from pprint import pprint
from .models import Paper
from .models import Problem
from .models import Record
from .models import Ans_Pic
from .models import Pro_Pic
from .models import Option
import random
import json
# Create your views here.

# choose the course
@csrf_exempt
def course(request):
    if (request.method == "GET") :
        if(request.GET.get("course")):
            course_type = request.GET.get("course")
            # if course_type == -1 return all papers
            if(course_type == "-1"):
                papers = []
                count = 0
                all_paper = Paper.objects.all()
                for paper in all_paper:
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
                return JsonResponse(return_dict)

            paper_set = Paper.objects.filter(paper_type=course_type)
            if(len(paper_set) == 0):
                return_msg = {
                    "success": 0,
                    "err_msg": "没有查询到相应学科"
                }
                return JsonResponse(return_msg)
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
            return JsonResponse(return_dict)
        else:
            return_msg = {
                "success": 0,
                "err_msg": "参数不正确"
            }
            return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg": "方法不正确"
        }
        return JsonResponse(return_msg)

# choose the paper
@csrf_exempt
def paper(request):
    if(request.method == "GET"):
        if(request.GET.get("paperId")):
            paper_id = request.GET.get("paperId")
            problems = Problem.objects.filter(paper = paper_id)
            if(len(problem) == 0):
                return_msg = {
                    "success": 0,
                    "err_msg": "没有查询到相应的试卷"
                }
                return JsonResponse(return_msg)
            count = 0
            problem_list = []
            for problem in problems:
                problem_dict = {}
                problem_dict['ProblemId'] = model_to_dict(problem)['id']
                problem_dict['ProblemOrder'] = model_to_dict(problem)['pro_order']
                count += 1
                problem_list.append(problem_dict)
            return_dict = {
                "success": 1,
                "ProblemNum": count,
                "Problems":problem_list
            }
            return JsonResponse(return_dict)
        else:
            return_msg = {
                "success": 0,
                "err_msg": "参数不正确"
            }
            return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg": "方法不正确"
        }
        return JsonResponse(return_msg)

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
            return JsonResponse(return_msg)
        else:
            return_msg = {
                "success": 0,
                "err_msg": "确保参数名完整"
            }
            return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg": "请检查方法"
        }
        return JsonResponse(return_msg)

#choose the problem 
@csrf_exempt
def problem(request):
    if(request.method == "GET"):
        if(request.GET.get("ProblemId")):
            ProblemId = request.GET.get("ProblemId")
            problem = model_to_dict(Problem.objects.get(id = ProblemId))
            problem.pop("paper")
            pprint(problem)
            if(problem["pro_type"] == 1 or problem["pro_type"] == 2):
                option_list = []
                if(problem["pro_type"] == 1):
                    Options = Option.objects.filter(problem__id = ProblemId)
                    for option in Options:
                        option_list.append(model_to_dict(option)['option']) 
                        problem['option'] = option_list
                problem.pop("pro_ans")
            problem['success'] = 1
            return JsonResponse(problem)
        else:
            return_msg = {
                "success" : 0,
                "err_msg" : "参数不正确"
            }
            return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg": "方法不正确"
        }
        return JsonResponse(return_msg)

@csrf_exempt
def record(request):
    #add the problem into the record
    if(request.method == "POST"):
        data = json.loads(request.body)
        problemId = data['ProblemId']
        username = data['username']
        note = data['username']
        courseType = data['courseType']
        Record.objects.create(pro_id = problemId, pro_User = username, pro_note = note,course = courseType)
        return_msg = {
            "success":1
        }
        return JsonResponse(return_msg)
    #check the user problem record
    elif(request.method == "GET"):
        if(request.GET.get("username") and request.GET.get("courseType")):
            username = request.GET.get("username")
            course = request.GET.get("courseType")
            records = Record.objects.filter(pro_User = username, course=course)
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
            return JsonResponse(return_msg)
    #delete this record
    elif(request.method == "DELETE"):
        data = json.loads(request.body)
        username = data['username']
        id = data['problemId']
        try:
            record = Record.objects.get(pro_User=username, pro_id=id)
            record.delete()
            return_msg = {
                "success": 1
            }
        except:
            return_msg = {
                "success": 0,
                "err_msg": "没有收藏这道错题"
            }
        return JsonResponse(return_msg)
    elif(request.method == "PUT"):
        data = json.loads(request.body)
        username = data['username']
        id = data['problemId']
        note = data['note']
        try:
            record = Record.objects.get(pro_User = username, pro_id=id)
            record.note = note
            record.save()
            return_msg = {
                "success": 1
            }
        except:
            return_msg = {
                "success": 0,
                "err_msg": "未加入错题本"
            } 
        return JsonResponse(return_msg)
#choose the inifite model
@csrf_exempt
def inifite(request):
    if(request.method == "GET"):
        if(request.GET.get("infinite") and request.GET.get("course_type")):
            if(request.GET.get("infinite") != "1"):
                return_msg = {
                    "success": 0,
                    "err_msg": "请确定请求内容是否正确"
                }
                return JsonResponse(return_msg)
            else:
                course = request.GET.get("course_type")
                problems = Problem.objects.filter(course_type = course)
                problemList= list(problems)
                random_problem = random.sample(problemList, 20)
                pprint(random_problem)
                return_pro = []
                count = 0;
                for problem in random_problem:
                    dict = {}
                    dict["ProblemId"] = model_to_dict(problem)['id']
                    dict["ProblemOrder"] = count
                    count += 1
                    return_pro.append(dict)
                return_msg = {
                    "success": 1,
                    "Problems": return_pro
                }
                return JsonResponse(return_msg)
        else:
            return_msg = {
                "success": 0,
                "err_msg": "检查参数"
            }
            return JsonResponse(return_msg)
    else:
        return_msg = {
            "success": 0,
            "err_msg":"检查请求方法"
        }
        return JsonResponse(return_msg)