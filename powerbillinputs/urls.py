from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import programs.views as views
import powerbillinputs.ajaxviews as ajaxviews


urlpatterns = [
   
    path('save_energy_charge/', ajaxviews.save_energy_charge_page, name='save_energy_charge'),
    path('show_energy_charges/', ajaxviews.show_energy_charges_page, name='show_energy_charges'),
    path('delete_energy_charge/', ajaxviews.delete_energy_charge_page, name='delete_energy_charge'),
    path('edit_energy_charge/', ajaxviews.edit_energy_charge_page, name='edit_energy_charge'),
    path('save_demand_charge/', ajaxviews.save_demand_charge_page, name='save_demand_charge'),
    path('show_demand_charges/', ajaxviews.show_demand_charges_page, name='show_demand_charges'),
    path('delete_demand_charge/', ajaxviews.delete_demand_charge_page, name='delete_demand_charge'),
    path('edit_demand_charge/', ajaxviews.edit_demand_charge_page, name='edit_demand_charge'),
    path('save_fixed_charge/', ajaxviews.save_fixed_charge_page, name='save_fixed_charge'),
    path('show_fixed_charges/', ajaxviews.show_fixed_charges_page, name='show_fixed_charges'),
    path('delete_fixed_charge/', ajaxviews.delete_fixed_charge_page, name='delete_fixed_charge'),
    path('edit_fixed_charge/', ajaxviews.edit_fixed_charge_page, name='edit_fixed_charge'),
    
    
    

]