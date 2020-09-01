from django.db import models
from inputs.models import YES_NO_CHOICES, TIMES_CHOICES
from scenarios.models import Scenario
# Create your models here.

ENERGY_TARIFF_TYPE_CHOICES = [
    ('Peak','Peak'),
    ('Offpeak','Offpeak'),
    ('Flat','Flat'),
]

DEMAND_TARIFF_TYPE_CHOICES = [
    ('Monthly Peak','Monthly Peak'),
    ('Capacity','Capacity'),    
]

CHARGEABLE_POWER_TYPE_CHOICES = [
    ('kW','kW'),
    ('kVA','kVA')
]

CATEGORY_CHOICES = [
    ('Retail','Retail'),
    ('Network','Network'),
    ('Marketing','Marketing'),
    ('Environmental','Environmental'),
    ('Metering','Metering'),
    ('Others','Others'),
]

FREQUENCY_CHOICES = [
    ('Daily','Daily'),
    ('Monthly','Monthly'),    
]

class EnergyCharge(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    tariff_name = models.CharField(max_length=15)
    include = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    amount = models.DecimalField(max_digits=5, decimal_places=4)
    tariff_type = models.CharField(max_length=10, choices=ENERGY_TARIFF_TYPE_CHOICES)
    weekday_start_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    weekday_end_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    weekend_start_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    weekend_end_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    months = models.CharField(max_length=30)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return ("Energy Charges - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)
        unique_together = ['scenario','tariff_name']


class DemandCharge(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    tariff_name = models.CharField(max_length=15)
    include = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    chargeable_power = models.DecimalField(max_digits=8,decimal_places=2)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    tariff_type = models.CharField(max_length=15, choices=DEMAND_TARIFF_TYPE_CHOICES)
    weekday_start_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    weekday_end_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    weekend_start_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    weekend_end_time = models.CharField(max_length=10, choices=TIMES_CHOICES)
    chargeable_power_type = models.CharField(max_length=4, choices=CHARGEABLE_POWER_TYPE_CHOICES)
    months = models.CharField(max_length=30)
    threshold = models.CharField(max_length=30)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return ("Demand Charges - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)
        

class FixedCharge(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    tariff_name = models.CharField(max_length=15)
    include = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return ("Fixed Charges - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)
        unique_together = ['scenario','tariff_name']


