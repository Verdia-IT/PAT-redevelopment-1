from django.contrib import admin
from .models import SolarLayout, SolarPrice, PFCPrice
# Register your models here.

admin.site.register(SolarLayout)
admin.site.register(SolarPrice)
admin.site.register(PFCPrice)
