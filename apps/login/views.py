from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'login/index.html')

def loginpage(request):
    return render(request, 'login/login.html')

def registerpage(request):
    return render(request, 'login/register.html')

def register(request):
    if request.method == "POST":
        print("new user registered")
        reg_errors = User.objects.reg_validator(request.POST)
        if len(reg_errors) > 0:
            for key, value in reg_errors.items():
                messages.warning(request, value)
            return redirect("/registerpage")
        else:
            newUserFirstName = request.POST['firstname']
            newUserLastName = request.POST['lastname']
            newUserEmail = request.POST['email']
            newUserPassword = request.POST['password']
            pwhash = bcrypt.hashpw(newUserPassword.encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name=newUserFirstName,last_name=newUserLastName,email=newUserEmail,password=pwhash)
            user = User.objects.filter(email=newUserEmail)
            logged_user = user[0]
            request.session['user_id'] = logged_user.id
            request.session['firstname'] = logged_user.first_name
            return redirect(f"/cookbook/{logged_user.id}")

def login(request):
    if request.method == "POST":
        log_errors = User.objects.login_validator(request.POST)
        if len(log_errors) > 0:
            for key, value in log_errors.items():
                messages.error(request, value)
            return redirect("/loginpage")
        else:
            email = request.POST['email']
            user = User.objects.filter(email=email)
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['user_id'] = logged_user.id
                    request.session['firstname'] = logged_user.first_name
                    # print("LOGIN"*100)
                    return redirect (f"/cookbook/{logged_user.id}")
                else:
                    pass
            return redirect("/loginpage")

def logout(request):
    request.session.clear()
    return redirect("/")

# Create your views here.
 