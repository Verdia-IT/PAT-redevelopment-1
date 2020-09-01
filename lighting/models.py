from django.db import models
from inputs.models import TIMES_CHOICES
from scenarios.models import Scenario
from references.models import ExistingLight, LedLight

# Create your models here.
class LightingHourDetail(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    lighting_type = models.CharField(max_length=25)
    monday_lighting_hour_1_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    monday_lighting_hour_1_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    monday_lighting_hour_2_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    monday_lighting_hour_2_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    tuesday_lighting_hour_1_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    tuesday_lighting_hour_1_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    tuesday_lighting_hour_2_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    tuesday_lighting_hour_2_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    wednesday_lighting_hour_1_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    wednesday_lighting_hour_1_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    wednesday_lighting_hour_2_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    wednesday_lighting_hour_2_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    thursday_lighting_hour_1_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    thursday_lighting_hour_1_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    thursday_lighting_hour_2_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    thursday_lighting_hour_2_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    friday_lighting_hour_1_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    friday_lighting_hour_1_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    friday_lighting_hour_2_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    friday_lighting_hour_2_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    saturday_lighting_hour_1_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    saturday_lighting_hour_1_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    saturday_lighting_hour_2_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    saturday_lighting_hour_2_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    sunday_lighting_hour_1_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    sunday_lighting_hour_1_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    sunday_lighting_hour_2_start = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')
    sunday_lighting_hour_2_end = models.CharField(max_length=15, choices=TIMES_CHOICES, default='N/A')

    def __str__(self):
        return (self.scenario.site_name.site_name + " " + self.scenario.scenario_name + " " + self.lighting_type)

    class Meta:
        unique_together = ['scenario','lighting_type']


class LightingInput(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    area = models.CharField(max_length=50, null=True, blank=True)
    lighting_type = models.ForeignKey(LightingHourDetail, on_delete=models.CASCADE)
    number_of_existing_luminaire = models.IntegerField()
    existing_luminaire = models.ForeignKey(ExistingLight, on_delete=models.CASCADE)
    existing_luminaire_power = models.DecimalField(max_digits=8,decimal_places=2)
    number_of_replaced_luminaire = models.IntegerField()
    replacement_luminaire = models.ForeignKey(LedLight, on_delete=models.CASCADE)
    replacement_luminaire_power = models.DecimalField(max_digits=8,decimal_places=1)
    power_reduction = models.DecimalField(max_digits=10,decimal_places=2)
    estimated_operating_hours = models.IntegerField()
    total_estimated_savings_kwhs = models.DecimalField(max_digits=10, decimal_places=2)
    veec_discount = models.DecimalField(max_digits=10 ,decimal_places=2)
    esc_discount = models.DecimalField(max_digits=10 ,decimal_places=2)
    discount_adjustment = models.DecimalField(max_digits=10 ,decimal_places=2)
    total_discount = models.DecimalField(max_digits=10 ,decimal_places=2)
    maintenance_savings = models.DecimalField(max_digits=10 ,decimal_places=2)
    dollar_per_fixture = models.DecimalField(max_digits=10,decimal_places=2)
    labour_per_hour = models.DecimalField(max_digits=10,decimal_places=2)
    fixtures_per_hour = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10 ,decimal_places=2)
    led_life_in_months = models.IntegerField()
    existing_lamp_replacement_costs = models.DecimalField(max_digits=10 ,decimal_places=2)
    existing_luminaire_life_in_months = models.IntegerField()
    
    def __str__(self):
        return (self.scenario.site_name.site_name + " " + self.scenario.scenario_name + " " + self.existing_luminaire.name)

    class Meta:
        ordering = ['id',]

class LightingOutput(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    number_of_lights = models.IntegerField()
    maintenance_savings = models.DecimalField(max_digits=10, decimal_places=2)
    power_reduction = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10 ,decimal_places=2)
    installation_cost = models.DecimalField(max_digits=10 ,decimal_places=2)
    other_adjustments_1 = models.DecimalField(max_digits=10 ,decimal_places=2)
    verdia_fee = models.DecimalField(max_digits=5 ,decimal_places=2)
    verdia_fee_dollars = models.DecimalField(max_digits=10 ,decimal_places=2)
    other_adjustments_2 = models.DecimalField(max_digits=10 ,decimal_places=2)
    total_cost = models.DecimalField(max_digits=10 ,decimal_places=2)  
    
    def __str__(self):
        return (self.scenario.site_name.site_name + " " + self.scenario.scenario_name + " " + str(self.number_of_lights))

    class Meta:
        ordering = ['id',]
