from django.contrib import admin
from django.urls import path

# import programs.views as views
import lighting.ajaxviews as ajaxviews
import lighting.views as views
import lighting.suggestions as suggestions


urlpatterns = [
   
    # ---------------------ajaxviews--------------------------------
    path('save_lighting_hour_detail/', ajaxviews.save_lighting_hour_detail_page, name='save_lighting_hour_detail'),
    path('show_lighting_hour_details/', ajaxviews.show_lighting_hour_details_page, name='show_lighting_hour_details'),
    path('delete_lighting_hour_detail/', ajaxviews.delete_lighting_hour_detail_page, name='delete_lighting_hour_detail'),
    path('edit_lighting_hour_detail/', ajaxviews.edit_lighting_hour_detail_page, name='edit_lighting_hour_detail'),

    path('save_lighting_input/', ajaxviews.save_lighting_input_page, name='save_lighting_input'),
    path('show_lighting_inputs/', ajaxviews.show_lighting_inputs_page, name='show_lighting_inputs'),
    path('delete_lighting_input/', ajaxviews.delete_lighting_input_page, name='delete_lighting_input'),
    path('edit_lighting_input/', ajaxviews.edit_lighting_input_page, name='edit_lighting_input'),
    path('lighting_outputs_calculation/', ajaxviews.lighting_outputs_calculation_page, name='lighting_outputs_calculation'),
    path('save_lighting_output/', ajaxviews.save_lighting_output_page, name='save_lighting_output'),

    # ---------------------suggestions--------------------------------
    # path('lighting_type_change/', suggestions.lighting_type_change_page, name='lighting_type_change'),
    path('existing_luminaire_change/', suggestions.existing_luminaire_change_page, name='existing_luminaire_change'),
    path('replacement_luminaire_change/', suggestions.replacement_luminaire_change_page, name='replacement_luminaire_change'),
    path('lighting_input_calculation/', suggestions.lighting_input_calculation_page, name='lighting_input_calculation'),
       
 

]