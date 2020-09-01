from django.db import models
import os

from scenarios.models import Scenario
from inputs.models import YES_NO_CHOICES
# Create your models here.

SYSTEM_TYPE_OVERRIDE_CHOICES = [
    ('No override', 'No Override'),
    ('LGC','LGC')
]

def layout_file_name(instance, filename):    
    return os.path.join('Solar Layout', instance.file_name)

class SolarLayout(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50)
    solar_layout_file = models.FileField(upload_to=layout_file_name)

    def __str__(self):
        return self.file_name
    
    class Meta:
        unique_together = ['scenario', 'file_name']


class SolarPrice(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    solar_size = models.DecimalField(max_digits=10, decimal_places=3)
    solar_unit_cost = models.DecimalField(max_digits=5, decimal_places=3)
    solar_unit_cost_override = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    gross_system_cost = models.DecimalField(max_digits=12 ,decimal_places=2)
    other_adjustments_1 = models.DecimalField(max_digits=10 ,decimal_places=2)
    verdia_fee = models.DecimalField(max_digits=5 ,decimal_places=2)
    verdia_fee_dollars = models.DecimalField(max_digits=10 ,decimal_places=2)
    other_adjustments_2 = models.DecimalField(max_digits=10 ,decimal_places=2)
    system_type = models.CharField(max_length=5)
    system_type_override = models.CharField(max_length=15, choices=SYSTEM_TYPE_OVERRIDE_CHOICES)
    stc_deeming_period = models.IntegerField()
    stc_discount = models.DecimalField(max_digits=10, decimal_places=2)
    system_cost = models.DecimalField(max_digits=12,decimal_places=2)
    system_unit_cost = models.DecimalField(max_digits=5, decimal_places=3)
    maintenance_cost_per_annum = models.DecimalField(max_digits=10,decimal_places=2)
    include_solar_maintenance = models.CharField(max_length=5,choices=YES_NO_CHOICES)

    def __str__(self):
        return self.scenario.scenario_name + " " + str(self.solar_size) + " " + str(self.system_cost)


class PFCPrice(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    pfc_size = models.IntegerField()
    pfc_unit_cost = models.DecimalField(max_digits=6, decimal_places=2)
    pfc_unit_cost_override = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    gross_system_cost = models.DecimalField(max_digits=12 ,decimal_places=2)    
    verdia_fee = models.DecimalField(max_digits=5 ,decimal_places=2)
    verdia_fee_dollars = models.DecimalField(max_digits=10 ,decimal_places=2)    
    system_cost = models.DecimalField(max_digits=12,decimal_places=2)
    system_unit_cost = models.DecimalField(max_digits=6, decimal_places=2)    

    def __str__(self):
        return self.scenario.scenario_name + " " + str(self.pfc_size) + " " + str(self.system_cost)


