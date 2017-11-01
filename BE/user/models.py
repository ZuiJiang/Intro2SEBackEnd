from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# Create your models here.
class UserManger(BaseUserManager):
    def create_user(self, phone, name, password=None):
        if not phone:
            raise ValueError("user must have an email")
        if not name:
            raise ValueError("user must have a name")
        user = self.model(
            phone = self.normalize_phone(phone),
            name = name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
class User(AbstractBaseUser):
    nickname = models.CharField(max_length = 32)
    password = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 13)
    problem_num = models.IntegerField(max_length = 10000, default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    object = UserManger()
    USERNAME_FIELD = 'phone'
    def get_nickname(self):
        return self.nickname
    def __str__(self):
        return self.nickname
    def get_phone(self):
        return self.phone
    def get_Problem_Num(self):
        return self.problem_num
    def has_perm(self, perm, obj = None):
        return True
    @property
    def is_staff(self):
        return self.is_admin