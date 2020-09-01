from django.db import models
from sites.models import Site
from programs.models import Program
import os

# Create your models here.
class Scenario(models.Model):
    scenario_name = models.CharField(max_length=50)
    site_name = models.ForeignKey(Site, on_delete=models.CASCADE)
    program_name = models.ForeignKey(Program, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)  
    chosen = models.BooleanField(blank=True, null=True, default=False) 

    def __str__(self):
        return self.program_name.program_name + " " + self.site_name.site_name  + " " + self.scenario_name

    class Meta:
        ordering = ('scenario_name',)
        unique_together = ['program_name', 'site_name', 'scenario_name']


def content_file_name(instance, filename):
    # ext = filename.split('.')[-1]
    # filename = "%s.%s" % (instance.file_name, ext)
    return os.path.join('Interval Data', instance.file_name)

class IntervalData(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50)
    interval_data_file = models.FileField(upload_to=content_file_name)

    def __str__(self):
        return self.file_name


