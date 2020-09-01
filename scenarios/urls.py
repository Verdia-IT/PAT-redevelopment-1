from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import programs.views as views
import scenarios.ajaxviews as ajaxviews
import scenarios.views as views


urlpatterns = [
   
    path('main_scenario/', views.main_scenario_page, name='main_scenario'),
    path('save_new_scenario/', ajaxviews.save_new_scenario_page, name='save_new_scenario'),
    path('show_scenarios/', ajaxviews.show_scenarios_page, name='show_scenarios'),
    path('delete_scenario/', ajaxviews.delete_scenario_page, name='delete_scenario'),
    path('choose_scenario/', ajaxviews.choose_scenario_page, name='choose_scenario'),
    
    path('interval_data_upload/', ajaxviews.interval_data_upload_page, name='interval_data_upload'),
    path('file_list/', ajaxviews.file_list_page, name='file_list'),
    path('delete_interval_data/', ajaxviews.delete_interval_data_page, name='delete_interval_data'),
    path('graph_interval_data/', ajaxviews.graph_interval_data_page, name='graph_interval_data'),    
 

]