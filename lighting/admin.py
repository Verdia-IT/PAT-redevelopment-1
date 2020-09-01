from django.contrib import admin
from .models import LightingHourDetail, LightingInput, LightingOutput

# Register your models here.
admin.site.register(LightingHourDetail)
admin.site.register(LightingInput)
admin.site.register(LightingOutput)
