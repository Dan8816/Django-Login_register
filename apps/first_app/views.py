from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from apps.first_app.models import User, UserManager
from django.contrib import messages
import re, bcrypt

def index(request):
    return render(request, 'first_app/index.html')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
            print(errors)
            return redirect('/')
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['confirmpassword'].encode(), bcrypt.gensalt())
        )
        print("successfully created users")
        request.session['first_name']=request.POST['first_name']
        return redirect('/success')    

def login(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print('email and password matches, successful login')
            request.session['first_name'] = user.first_name
            return redirect('/success')
        else:
            print("failed password")

def success(request):
    return render(request, "first_app/success.html")

def logout(request):
    request.session.clear()    
    return redirect('/')