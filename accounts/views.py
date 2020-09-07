from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import RegisterUserForm, LoginForm, RegisterProfileForm
import os
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.
def login_page(request):
    redirect_path = "/dashboard/"
    error_message = ""
    user = request.user
    if user.is_authenticated:
        return redirect(redirect_path)
    form = LoginForm(request.POST or None)
    if request.method == "POST":        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request,user)
                return redirect(redirect_path)
            else:
                error_message = "* Error! Email and Password do not match! Please try again."
    
    context = {
        "form": form,
        "error_message":error_message,
    }  
    request.session['logout_message'] =  ""  
        
    return render(request,"auth/login.html", context)


def register_page(request):
    redirect_path = "/login/"
    user = request.user
    if user.is_authenticated:
        return redirect(redirect_path)
    form_user = RegisterUserForm(request.POST or None)
    form_profile = RegisterProfileForm(request.POST or None, request.FILES or None)
    context = {
        "form_user": form_user,
        "form_profile": form_profile,
    }
    if request.method == "POST":
        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save()
            obj_profile = form_profile.save(commit=False)
            obj_profile.user = user
            obj_profile.save()
            return redirect(redirect_path)
    return render(request, "auth/register.html" ,context)

def logout_page(request):
    # print('User:', request.user)
    logout(request)    
    # print('User:', request.user)
    request.session['logout_message'] =  "* You have been successfully logged out. Please Sign in again"
    return redirect("/")

def profile_page(request):
    context = {}
    return render(request,"auth/profile.html",context)


@login_required(login_url="/")
def profile_page1(request):
    # user = request.user   
     
    profile = request.user.profile
    old_path = profile.image.path
    form_profile = RegisterProfileForm(instance=profile)

    if request.method == "POST":      
        form_profile = RegisterProfileForm(request.POST, request.FILES or None, instance=profile)
        if form_profile.is_valid():
            if request.FILES:             
                os.remove(old_path)
            form_profile.save()  
    
    context = {
        'user':request.user,
        'form_profile':form_profile,
    }
    return render(request,"auth/profile.html",context)