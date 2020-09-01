from django.contrib import admin
from .models import (CertificatePrices, TariffEscalations, PeakEnergyRates, OffpeakEnergyRates, LightingData, SolarData,
                     LedLight, ExistingLight, SolarCost, PFCCost, PostcodeResource)


class PostcodeResourceAdmin(admin.ModelAdmin):
    list_display  = ('postcode', 'suburb', 'state', 'latitude','longitude','emissions_factor','stc_zone','rating','pvsyst_generation_factor')


# Register your models here.
admin.site.register(CertificatePrices)
admin.site.register(TariffEscalations)
admin.site.register(PeakEnergyRates)
admin.site.register(OffpeakEnergyRates)
admin.site.register(LightingData)
admin.site.register(LedLight)
admin.site.register(ExistingLight)
admin.site.register(SolarCost)
admin.site.register(PFCCost)
admin.site.register(PostcodeResource,PostcodeResourceAdmin)
admin.site.register(SolarData)


