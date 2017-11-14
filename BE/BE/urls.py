"""BE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from user import views as user
from course import views as course 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/register/$',user.register, name="register"),
    url(r'^user/login/$',user.login, name="login"),
    url(r'^user/sendEmail/$',user.sendEmail, name="sendEmail"),
    url(r'^user/password/$',user.password, name="password"),
    url(r'^course/course/$',course.course, name="course"),
    url(r'^course/paper/$',course.paper, name="paper"),
    url(r'^course/problem/$',course.problem, name="problem"),
    url(r'^course/record/$',course.record, name="record"),
    url(r'^course/judge/$',course.judge, name="judge"),
    url(r'^course/infinite/$',course.inifite, name="infinite"),
]
