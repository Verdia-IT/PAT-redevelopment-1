from django.contrib import admin
from django.urls import path

# import programs.views as views
import solarpfc.ajaxviews as ajaxviews


urlpatterns = [
   
    # ---------------------ajaxviews--------------------------------
    path('solar_price_calculation/', ajaxviews.solar_price_calculation_page, name='solar_price_calculation'),
    path('save_solar_price/', ajaxviews.save_solar_price_page, name='save_solar_price'),
    # path('solar_unit_cost_calculation/', ajaxviews.solar_unit_cost_calculation_page, name='solar_unit_cost_calculation'),
    path('solar_layout_upload/', ajaxviews.solar_layout_upload_page, name='solar_layout_upload'),
    path('pfc_price_calculation/', ajaxviews.pfc_price_calculation_page, name='pfc_price_calculation'),
    path('save_pfc_price/', ajaxviews.save_pfc_price_page, name='save_pfc_price'),

 

]