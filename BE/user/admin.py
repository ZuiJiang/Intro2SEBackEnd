from django.contrib import admin
from .models import Profile
from .models import Email
# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ("email","validate")
admin.site.register(Profile)
admin.site.register(Email, EmailAdmin)