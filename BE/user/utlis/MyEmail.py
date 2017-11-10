from random import Random
from django.core.mail import send_mail
from BE.settings import DEFAULT_FROM_EMAIL
def generate_random_str(random_length=4):
    random_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkIiMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        random_str += chars[random.randint(0,length)]
    return random_str
def send_your_email(email):
    email_title = '啦啦啦啦测试'
    validate = generate_random_str(4)
    email_body = "你的验证码是{0}".format(validate)
    send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
    if send_status:
        return validate
    else:
        return -1 
