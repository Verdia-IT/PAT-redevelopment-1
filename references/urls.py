from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import references.views as views
import references.ajaxviews as ajaxviews


urlpatterns = [
   
    path('', views.references_page, name='references'),
    path('save_certificate/', ajaxviews.save_certificate_page, name='save_certificate'),
    path('save_tariff_escalations/', ajaxviews.save_tariff_escalations_page, name='save_tariff_escalations'),
    path('save_peak_energy_rates/', ajaxviews.save_peak_energy_rates_page, name='save_peak_energy_rates'),
    path('save_offpeak_energy_rates/', ajaxviews.save_offpeak_energy_rates_page, name='save_offpeak_energy_rates'),
    path('save_lighting_data/', ajaxviews.save_lighting_data_page, name='save_lighting_data'),
    path('save_led/', ajaxviews.save_led_page, name='save_led'),
    path('delete_led/', ajaxviews.delete_led_page, name='delete_led'),
    path('edit_led/', ajaxviews.edit_led_page, name='edit_led'),
    path('show_led_database/', ajaxviews.show_led_database_page, name='show_led_database'),
    path('save_existing/', ajaxviews.save_existing_page, name='save_existing'),
    path('delete_existing/', ajaxviews.delete_existing_page, name='delete_existing'),
    path('edit_existing/', ajaxviews.edit_existing_page, name='edit_existing'),
    path('show_existing_database/', ajaxviews.show_existing_database_page, name='show_existing_database'),
    path('fill_existing_led_replacement/', ajaxviews.fill_existing_led_replacement_page, name='fill_existing_led_replacement'),
    path('save_solar_cost/', ajaxviews.save_solar_cost_page, name='save_solar_cost'),
    path('show_solar_cost/', ajaxviews.show_solar_cost_page, name='show_solar_cost'),
    path('delete_solar_cost/', ajaxviews.delete_solar_cost_page, name='delete_solar_cost'),
    path('edit_solar_cost/', ajaxviews.edit_solar_cost_page, name='edit_solar_cost'),
    path('save_pfc_cost/', ajaxviews.save_pfc_cost_page, name='save_pfc_cost'),
    path('show_pfc_cost/', ajaxviews.show_pfc_cost_page, name='show_pfc_cost'),
    path('delete_pfc_cost/', ajaxviews.delete_pfc_cost_page, name='delete_pfc_cost'),
    path('edit_pfc_cost/', ajaxviews.edit_pfc_cost_page, name='edit_pfc_cost'),
    path('download_data/', ajaxviews.download_data_page, name='download_data'),
    path('solar_data_upload/', ajaxviews.solar_data_upload_page, name='solar_data_upload'),

    

]


