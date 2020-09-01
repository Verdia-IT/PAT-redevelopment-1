from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import programs.views as views
import inputs.ajaxviews as ajaxviews


urlpatterns = [
   
    path('save_bill_detail/', ajaxviews.save_bill_detail_page, name='save_bill_detail'),
    path('save_operating_hour_detail/', ajaxviews.save_operating_hour_detail_page, name='save_operating_hour_detail'),
    path('save_holiday_detail/', ajaxviews.save_holiday_detail_page, name='save_holiday_detail'),
    path('save_price_forecast_override/', ajaxviews.save_price_forecast_override_page, name='save_price_forecast_override'),
    path('save_escalations_override/', ajaxviews.save_escalations_override_page, name='save_escalations_override'),
    path('save_solar_export/', ajaxviews.save_solar_export_page, name='save_solar_export'),
    
    

]