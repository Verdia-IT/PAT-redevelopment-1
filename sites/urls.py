from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import programs.views as views
import sites.ajaxviews as ajaxviews
import sites.views as views


urlpatterns = [
   
    path('main_site/', views.main_site_page, name='main_site'),
    path('save_new_site/', ajaxviews.save_new_site_page, name='save_new_site'),
    path('show_sites/', ajaxviews.show_sites_page, name='show_sites'),
    path('delete_site/', ajaxviews.delete_site_page, name='delete_site'),
    path('include_site/', ajaxviews.include_site_page, name='include_site'),

]