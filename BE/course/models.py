from django.db import models

# Create your models here.
class Paper(models.Model):
    # django will have a default auto-increase key named id
    # we use it to stands for the paper id which is only
    # paper_desc is for the paper's description something like 
    # Advanced Mathmatics 2016 
    # paper_num is for the paper's totally problems 
    # paper_course is for the paper's course  
    # paper_type is for the type of the paper
    # like the advanced mathmatics
    # paper_year is the year of the paper
    paper_title = models.CharField(max_length = 100)
    problem_num = models.IntegerField()
    paper_course = models.CharField(max_length = 20)
    paper_type = models.IntegerField() 
    paper_year = models.CharField(max_length = 5)
    def __str__(self):
        return self.paper_title
    def get_paper_course(self):
        return self.paper_course
    
class Problem(models.Model):
    # we use the default id to representative the problem Id 
    # which is the unique
    # pro_des is the problem description like 2016 Advanced Math the first problem
    # pro_detail is the problem detail 
    # course_type is the problem belongs course
    # pro_ans is the problem answer
    # pro_img is the problem image
    # ans_img is the answer image
    # pro_order is the order in paper 
    # pro_type is the type 1 for the choose proble
    # 2 for the judge problem, 3 for tiankong problem
    # 4 for the Big Problem
    paper = models.ForeignKey('course.Paper')
    course_type = models.IntegerField()
    pro_des = models.TextField()
    pro_detail = models.TextField()
    pro_ans = models.TextField()
    pro_order = models.IntegerField()
    pro_type = models.IntegerField()
    def __str__(self):
        return self.pro_ans
    def get_correct_ans(self):
        return self.pro_ans

class Record(models.Model):
    pro_User = models.CharField(max_length=10)
    pro_id = models.CharField(max_length=10) 
    pro_note = models.TextField()
    course = models.IntegerField()
    def __str__(self):
        return self.pro_User
    def get_record_note(self):
        return self.pro_note
    def get_record_id(self):
        return self.pro_id

class Pro_Pic(models.Model):
    problem = models.ForeignKey('course.Problem')
    ans_pic_url = models.URLField()
    def __str__(self):
        return self.problem.pro_des

class Ans_Pic(models.Model):
    problem = models.ForeignKey('course.Problem')
    pro_pic_url = models.URLField()
    def __str__(self):
        return self.problem.pro_des

class Option(models.Model):
    problem = models.ForeignKey('course.Problem')
    option = models.CharField(max_length = 30)
    order = models.CharField(max_length = 3)
    def __str__(self):
        return self.problem.pro_des