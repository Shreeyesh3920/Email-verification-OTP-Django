from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import string
import random
# Create your views here.

def home(request):
    return render(request , 'home.html')
def login(request):
 return render(request , 'login.html')



def register(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            
            chars=''.join((string.digits))
            conf_code=''.join(random.choice(chars) for _ in range(6))
            
            profile_obj = Profile.objects.create(user = user_obj , code=conf_code)
            profile_obj.save()
            send_mail_after_registration(email ,conf_code)
            return redirect('/token')
        except Exception as e:
            print(e)
    return render(request , 'register.html')   
    
    
    
def success(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            profile_obj = Profile.objects.filter(code=code).first()
        
            if profile_obj:
                profile_obj.is_verified=True
                profile_obj.save()
                messages.success(request, 'Your account has been  verified.')
                return redirect('/login')
            else:
                messages.success(request, 'Wrong OTP! Please enter Correct OTP.')
                return redirect('/token')
        except Exception as e:
            print(e)
        
    
def token(request):
    return render(request , 'token.html')     


def send_mail_after_registration(email,conf_code):
    
    subject = 'Your accounts need to be verified'
    message = f'Your OTP code is {conf_code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )    