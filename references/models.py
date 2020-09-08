from django.db import models
from rest_framework import serializers
from sites.models import STATE_CHOICES
import os
# Create your models here.


class CertificatePrices(models.Model):
    STCprice = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    VEECprice = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    ESCprice = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2019 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2020 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2021 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2022 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2023 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2024 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2025 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2026 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2027 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2028 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2029 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2030 = models.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)


class TariffEscalations(models.Model):
    year = models.IntegerField()
    queensland = models.DecimalField(max_digits=4, decimal_places=3)
    new_south_wales = models.DecimalField(max_digits=4, decimal_places=3)
    victoria = models.DecimalField(max_digits=4, decimal_places=3)
    south_australia = models.DecimalField(max_digits=4, decimal_places=3)
    western_australia = models.DecimalField(max_digits=4, decimal_places=3)
    australian_capital_territory = models.DecimalField(
        max_digits=4, decimal_places=3)
    tasmania = models.DecimalField(max_digits=4, decimal_places=3)
    northern_territory = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self):
        return str(self.year)


class PeakEnergyRates(models.Model):
    year = models.IntegerField()
    queensland = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    new_south_wales = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    victoria = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    south_australia = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    western_australia = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    australian_capital_territory = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    tasmania = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    northern_territory = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.year)


class OffpeakEnergyRates(models.Model):
    year = models.IntegerField()
    queensland = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    new_south_wales = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    victoria = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    south_australia = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    western_australia = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    australian_capital_territory = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    tasmania = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)
    northern_territory = models.DecimalField(
        blank=True, null=True, max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.year)


class LightingData(models.Model):
    verdia_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.verdia_fee)



class LedLight(models.Model):
    name = models.CharField(max_length=45, unique=True)
    # BATTEN = 'BT'
    # BULKHEAD = 'BH'
    # DOWNLIGHT = 'DL'
    # DECORATIVE = 'DE'
    # FLOODLIGHT = 'FL'
    # HIGHBAY = 'HB'
    # OTHER_FITTING_TYPE = 'OT'
    # OYSTER = 'OY'
    # PANEL = 'PN'
    # WEATHERPROOF = 'WP'
    FITTING_TYPE_CHOICES = [
        ('Batten', 'Batten'),
        ('Bulkhead', 'Bulkhead'),
        ('Downlight', 'Downlight'),
        ('Decorative', 'Decorative'),
        ('Floodlight', 'Floodlight'),
        ('Highbay', 'Highbay'),
        ('Other', 'Other'),
        ('Oyster', 'Oyster'),
        ('Panel', 'Panel'),
        ('Weatherproof', 'Weatherproof'),
    ]
    fitting_type = models.CharField(max_length=30, choices=FITTING_TYPE_CHOICES)
    # RECESSED_PLASTER = 'RP'
    # RECESSED_T_GRID = 'RTG'
    # SURFACE_MOUNT = 'SM'
    # SUSPENDED = 'SUS'
    # WALL_MOUNT = 'WM'
    # OTHER_INSTALL_TYPE = 'OIT'
    INSTALLATION_TYPE_CHOICES = [
        ('Recessed Plaster', 'Recessed Plaster'),
        ('Recessed T-Grid', 'Recessed T-Grid'),
        ('Surface Mount', 'Surface Mount'),
        ('Suspended', 'Suspended'),
        ('Wall Mount', 'Wall Mount'),
        ('Other', 'Other'),
    ]
    installation_type = models.CharField(
        max_length=30, choices=INSTALLATION_TYPE_CHOICES)
    system_power = models.DecimalField(max_digits=5, decimal_places=1)
    led_life = models.IntegerField()
    replacement_fitting_price = models.DecimalField(
        max_digits=7, decimal_places=2)
    replacement_fittings_per_hour = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ExistingLight(models.Model):
    name = models.CharField(max_length=45, unique=True)
    led_light = models.ForeignKey(
        LedLight, related_name='existing_lights', on_delete=models.CASCADE)
    other_names = models.TextField(blank=True, null=True)    
    FITTING_TYPE_CHOICES = [
        ('Batten', 'Batten'),
        ('Bulkhead', 'Bulkhead'),
        ('Downlight', 'Downlight'),
        ('Decorative', 'Decorative'),
        ('Emergency Batten', 'Emergency Batten'),
        ('Floodlight', 'Floodlight'),
        ('Highbay', 'Highbay'),
        ('Other', 'Other'),
        ('Oyster', 'Oyster'),
        ('Troffer', 'Troffer'),
        ('Panel', 'Panel'),
        ('Weatherproof', 'Weatherproof'),
    ]
    fitting_type = models.CharField(max_length=30, choices=FITTING_TYPE_CHOICES)
    # RECESSED_PLASTER = 'RP'
    # RECESSED_T_GRID = 'RTG'
    # SURFACE_MOUNT = 'SM'
    # SUSPENDED = 'SUS'
    # WALL_MOUNT = 'WM'
    # OTHER_INSTALL_TYPE = 'OIT'
    INSTALLATION_TYPE_CHOICES = [
        ('Recessed Plaster', 'Recessed Plaster'),
        ('Recessed T-Grid', 'Recessed T-Grid'),
        ('Surface Mount', 'Surface Mount'),
        ('Suspended', 'Suspended'),
        ('Wall Mount', 'Wall Mount'),
        ('Other', 'Other'),
    ]
    installation_type = models.CharField(
        max_length=30, choices=INSTALLATION_TYPE_CHOICES)
    lamp_quantity = models.IntegerField()
    lamp_wattage = models.DecimalField(max_digits=5, decimal_places=1)
    system_power = models.DecimalField(max_digits=5, decimal_places=1)
    lamp_life = models.IntegerField()
    replacement_lamp_price = models.DecimalField(
        max_digits=7, decimal_places=2)
    replacement_lamp_fittings_per_hour = models.IntegerField()
    replacement_fitting_price = models.DecimalField(
        max_digits=7, decimal_places=2)
    replacement_fittings_per_hour = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class SolarCost(models.Model):
    system_size = models.IntegerField(unique=True)
    single_site_dollar_per_watt = models.DecimalField(
        max_digits=5, decimal_places=3)
    single_site_verdia_fee = models.DecimalField(
        max_digits=5, decimal_places=3)
    multi_site_dollar_per_watt = models.DecimalField(
        max_digits=5, decimal_places=3)
    multi_site_verdia_fee = models.DecimalField(
        max_digits=5, decimal_places=3)

    def __str__(self):
        return str(self.system_size) + ' kW'

    class Meta:
        ordering = ('system_size',)


class PFCCost(models.Model):
    pfc_rating = models.IntegerField(unique=True)
    pfc_dollar_per_kvar = models.DecimalField(
        max_digits=5, decimal_places=1)
    

    def __str__(self):
        return str(self.pfc_rating) + ' kvar'
    
    class Meta:
        ordering = ('pfc_rating',)


class PostcodeResource(models.Model):
    postcode = models.IntegerField()
    suburb = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    emissions_factor = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    stc_zone = models.IntegerField()
    rating = models.DecimalField(max_digits=4, decimal_places=3)
    pvsyst_generation_factor = models.DecimalField(max_digits=5, decimal_places=4)

    def __str__(self):
        return str(self.postcode)
    
    class Meta:
        ordering = ('postcode','suburb',)
        unique_together = ['postcode', 'suburb']


def solar_data_file_name(instance, filename):    
    return os.path.join('Solar Data', instance.file_name)

class SolarData(models.Model):    
    file_name = models.CharField(max_length=50)
    solar_data_file = models.FileField(upload_to=solar_data_file_name)

    def __str__(self):
        return self.file_name