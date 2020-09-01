from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import programs.views as views
import programs.ajaxviews as ajaxviews


urlpatterns = [
   
    path('', views.programs_page, name='programs'),
    path('save_new_program/', ajaxviews.save_new_program_page, name='save_new_program'),
    path('save_program_overrides/', ajaxviews.save_program_overrides_page, name='save_program_overrides'),
    path('show_programs/', ajaxviews.show_programs_page, name='show_programs'),
    path('run_simulations/', ajaxviews.run_simulations_page, name='run_simulations'),
    path('main_program/', views.main_program_page, name='main_program'),
]