from django.contrib import admin
from .models import SimulationParameter, SimulationOutput

# Register your models here.
admin.site.register(SimulationParameter)
admin.site.register(SimulationOutput)