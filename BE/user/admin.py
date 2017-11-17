from django.contrib import admin
from .models import Profile
from .models import Email
# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ("email","validate")
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","finishNum", "accuracy")
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Email, EmailAdmin)