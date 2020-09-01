from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/")
def home_page(request):
    return render(request, "home.html", {})


# class HomePage(View):
#     template_name = 'home.html'

#     def get(self, request):
#         return render(request, self.template_name)


# class LoginPage(View):
#     template_name = 'auth/login.html'

#     def get(self, request):
#         return render(request, self.template_name)





# class NewProgramPage(View):
#     template_name = 'new_program.html'

#     def get(self, request):
#         return render(request, self.template_name)


# class CurrentProgramsPage(View):
#     template_name = 'current_programs.html'

#     def get(self, request):
#         return render(request, self.template_name)


# class MainProgramPage(View):
#     template_name = 'main_program.html'

#     def get(self, request):
#         return render(request, self.template_name)


# def main_site_page(request):
#     return render(request, 'main_site.html',{'site_id':1})

# def main_scenario_page(request):
#     return render(request, 'main_scenario.html',{'scenario_id':1})


