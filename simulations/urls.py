from django.contrib import admin
from django.urls import path

# import programs.views as views
import simulations.ajaxviews as ajaxviews


urlpatterns = [
   
    # ---------------------ajaxviews--------------------------------
    path('save_simulation_parameter/', ajaxviews.save_simulation_parameter_page, name='save_simulation_parameter'),
    path('run_simulation/', ajaxviews.run_simulation_page, name='run_simulation'),
    path('run_iterations/', ajaxviews.run_iterations_page, name='run_iterations'),
    
    
 

]