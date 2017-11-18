from django.contrib import admin
from .models import Paper
from .models import Problem
from .models import Record
from .models import Pro_Pic
from .models import Ans_Pic
from .models import Option
# Register your models here.
class PaperAdmin(admin.ModelAdmin):
    list_display = ("id" ,'paper_title','problem_num','paper_course')
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("pro_des",'pro_order', "id")
class RecordAdmin(admin.ModelAdmin):
    list_display = ("pro_User","pro_id")
admin.site.register(Paper, PaperAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Pro_Pic)
admin.site.register(Ans_Pic)
admin.site.register(Option)