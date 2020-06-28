import pyotp
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
import time
from django.core.mail import EmailMessage

now = int(time.time())


def send_verification_email(email, msg):
    email_subject = 'OTP VERIFICATION!!!'
    email = EmailMessage(
        email_subject, msg, to=[email]
    )
    print("Email sent successfully!")
    email.send()


def u_login(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'err': 'Email does not found!'})
        time_otp = pyotp.TOTP(user.key, interval=900)
        time_otp = time_otp.now()
        send_verification_email(email, 'Your verification OTP is ' + time_otp)
        print(email, time_otp)
        if email:
            return render(request, 'verify.html', {'email': email})
    else:
        return render(request, 'login.html')


def verify(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        otp = request.POST.get('otp', None)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect('/')
        t = pyotp.TOTP(user.key, interval=900)
        is_verified = t.verify(otp)
        if is_verified:
            login(request, user)
        else:
            return render(request, 'verify.html', {'err': 'wrong otp', 'email': email})
        return redirect('/')
    else:
        return render(request, 'verify.html')


def welcome(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'welcome.html')


def u_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')
