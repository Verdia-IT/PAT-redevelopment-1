from django.db import models
from programs.models import Program

STATE_CHOICES = [
    ('new_south_wales', 'New South Wales'),
    ('northern_territory', 'Northern Territory'),
    ('queensland', 'Queensland'),
    ('victoria', 'Victoria'),
    ('south_australia', 'South Australia'),
    ('australian_capital_territory', 'Australian Capital Territory'),
    ('tasmania', 'Tasmania'),
    ('western_australia', 'Western Australia'),
]
DNSP_CHOICES = [
    ('Ausgrid', 'Ausgrid'),
    ('Citipower', 'Citipower'),
    ('Endeavour', 'Endeavour'),
    ('Energex', 'Energex'),
    ('Essential', 'Essential'),
    ('SAPN', 'SAPN'),
    ('Jemena', 'Jemena'),
    ('Powercor', 'Powercor'),
    ('Ausnet', 'Ausnet'),
    ('United Energy', 'United Energy'),
    ('Western Power', 'Western Power'),
    ('Horizon Power', 'Horizon Power'),
    ('ActewAGL', 'ActewAGL'),
]
INDUSTRY_TYPE_CHOICES = [
    ('Agriculture', 'Agriculture'),
    ('Mining', 'Mining'),
    ('Manufacturing', 'Manufacturing'),
    ('Electricity, Gas and Water Supply', 'Electricity, Gas and Water Supply'),
    ('Construction', 'Construction'),
    ('Wholesale Trade', 'Wholesale Trade'),
    ('Retail Trade', 'Retail Trade'),
    ('Accommodation, Cafes and Restaurants',
     'Accommodation, Cafes and Restaurants'),
    ('Transport and Storage', 'Transport and Storage'),
    ('Communication Services', 'Communication Services'),
    ('Finance and Insurance', 'Finance and Insurance'),
    ('Property and Business Services', 'Property and Business Services'),
    ('Government Administration and Defence',
     'Government Administration and Defence'),
    ('Education', 'Education'),
    ('Health and Community Services', 'Health and Community Services'),
    ('Cultural and Recreational Services',
     'Cultural and Recreational Services'),
    ('Personal and Other Services', 'Personal and Other Services'),

]
SOLAR_DATA_CHOICES = [
    ('Sydney', 'Sydney'),
    ('Melbourne', 'Melbourne'),
    ('Rockhampton', 'Rockhampton'),
    ('Adelaide', 'Adelaide'),
    ('Hobart', 'Hobart'),
    ('Perth', 'Perth'),
    ('Alice Springs', 'Alice Springs'),
]


class Site(models.Model):
    site_name = models.CharField(max_length=50)
    program_name = models.ForeignKey(Program, on_delete=models.CASCADE)
    NMI = models.CharField(max_length=13)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    postcode = models.IntegerField()
    DNSP = models.CharField(max_length=20, choices=DNSP_CHOICES)
    industry_type = models.CharField(
        max_length=40, choices=INDUSTRY_TYPE_CHOICES)
    default_solar_data = models.CharField(
        max_length=20, choices=SOLAR_DATA_CHOICES)
    included = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name

    class Meta:
        ordering = ('site_name',)
        unique_together = ['program_name', 'site_name']
