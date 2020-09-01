from django.contrib import admin
from .models import (BillDetail, OperatingHourDetail, HolidayDetail, SolarExport,
                     PriceForecastOverride, EscalationsOverride)

# Register your models here.
admin.site.register(BillDetail)
admin.site.register(OperatingHourDetail)
admin.site.register(HolidayDetail)
admin.site.register(PriceForecastOverride)
admin.site.register(EscalationsOverride)
admin.site.register(SolarExport)
