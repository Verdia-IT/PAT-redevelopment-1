from django.contrib import admin
from .models import EnergyCharge, DemandCharge, FixedCharge
# Register your models here.

admin.site.register(EnergyCharge)
admin.site.register(DemandCharge)
admin.site.register(FixedCharge)