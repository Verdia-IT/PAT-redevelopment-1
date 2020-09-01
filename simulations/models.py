from django.db import models
from scenarios.models import IntervalData

from inputs.models import YES_NO_CHOICES
from scenarios.models import Scenario
# Create your models here.



class SimulationParameter(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    interval_data = models.ForeignKey(IntervalData, on_delete=models.DO_NOTHING)
    include_lighting = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    solar_size = models.DecimalField(max_digits=10, decimal_places=3)
    pfc_size = models.DecimalField(max_digits=10,decimal_places=2)
    target_pf = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.scenario.scenario_name + " " + str(self.solar_size) + " kW"


class SimulationOutput(models.Model):
    scenario = models.OneToOneField(Scenario, on_delete=models.CASCADE, unique=True)
    npv = models.DecimalField(max_digits=10, decimal_places=2)
    irr = models.DecimalField(max_digits=6, decimal_places=4)
    payback = models.DecimalField(max_digits=4, decimal_places=2)
    lcoe = models.DecimalField(max_digits=5,decimal_places=4)

    def __str__(self):
        return self.scenario.program_name.program_name + " " + self.scenario.site_name.site_name + " " + self.scenario.scenario_name