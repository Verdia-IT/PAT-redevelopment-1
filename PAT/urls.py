"""Pat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import (home_page)

from references import urls as references_urls
from programs import urls as programs_urls
from sites import urls as sites_urls
from scenarios import urls as scenarios_urls
from inputs import urls as inputs_urls
from lighting import urls as lighting_urls
from powerbillinputs import urls as powerbillinputs_urls
from solarpfc import urls as solarpfc_urls
from simulations import urls as simulations_urls
from accounts.views import register_page, login_page, logout_page, profile_page


urlpatterns = [
    path('dashboard/', home_page, name='home'),
    path('', login_page, name='login'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('profile/', profile_page, name='profile'),
    # path('newprogram/', NewProgramPage.as_view(), name='new_program'),
    # path('mainprogram/', MainProgramPage.as_view(), name='main_program'),
    # path('mainsite/', main_site_page, name='main_site'),
    # path('mainscenario/', main_scenario_page, name='main_scenario'),    
    path('programs/',include(programs_urls)),
    path('sites/',include(sites_urls)),
    path('references/',include(references_urls)),
    path('scenarios/',include(scenarios_urls)),
    path('inputs/',include(inputs_urls)),
    path('lighting/',include(lighting_urls)),
    path('solarpfc/',include(solarpfc_urls)),
    path('simulations/',include(simulations_urls)),
    path('powerbillinputs/',include(powerbillinputs_urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
