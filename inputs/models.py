from django.db import models

# Create your models here.
from scenarios.models import Scenario


MONTH_CHOICES = [
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),

]

MONTH_2_CHOICES = [
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10),
    (11,11),
    (12,12),
]

ELECTRICIY_RETAILER_CHOICES = [
    ('1st energy', '1st energy'),
    ('ActewAGL', 'ActewAGL'),
    ('AGL Energy', 'AGL Energy'),
    ('Alinta Energy ', 'Alinta Energy '),
    ('Aurora Energy ', 'Aurora Energy '),
    ('Blue NRG', 'Blue NRG'),
    ('Click Energy ', 'Click Energy '),
    ('Commander', 'Commander'),
    ('Cova U', 'Cova U'),
    ('Dodo Power & Gas ', 'Dodo Power & Gas '),
    ('Diamond Energy ', 'Diamond Energy '),
    ('EnergyAustralia ', 'EnergyAustralia '),
    ('Ergon Energy ', 'Ergon Energy '),
    ('ERM Business Energy ', 'ERM Business Energy '),
    ('GloBird Energy', 'GloBird Energy'),
    ('Horizon Power', 'Horizon Power'),
    ('Lumo Energy', 'Lumo Energy'),
    ('Momentum Energy ', 'Momentum Energy '),
    ('Next Business Energy', 'Next Business Energy'),
    ('Origin Energy ', 'Origin Energy '),
    ('Pacific Hydro', 'Pacific Hydro'),
    ('People Energy', 'People Energy'),
    ('Perth Energy', 'Perth Energy'),
    ('Powerdirect', 'Powerdirect'),
    ('Powershop', 'Powershop'),
    ('Qenergy', 'Qenergy'),
    ('Red Energy ', 'Red Energy '),
    ('Sanctuary Energy', 'Sanctuary Energy'),
    ('Simply Energy ', 'Simply Energy '),
    ('Sumo Power', 'Sumo Power'),
    ('Synergy', 'Synergy'),
    ('Urth Energy', 'Urth Energy'),
    ('WinEnergy', 'WinEnergy'),
    ('Other', 'Other'),

]

TIMES_CHOICES = [
    ('All Times', 'All Times'),
    ('N/A', 'N/A'),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'),

]

YES_NO_CHOICES = [
    ('Yes','Yes'),
    ('No','No')
]

# Create your models here.


class BillDetail(models.Model):
    scenario = models.OneToOneField(Scenario, on_delete=models.CASCADE)
    number_of_bills = models.IntegerField()
    bill_month = models.CharField(max_length=10, choices=MONTH_CHOICES)
    bill_year = models.IntegerField()
    bill_days = models.IntegerField()
    electricity_retailer = models.CharField(
        max_length=30, choices=ELECTRICIY_RETAILER_CHOICES)
    kwhs_consumed = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return ("Bill Detail - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)


class OperatingHourDetail(models.Model):
    scenario = models.OneToOneField(Scenario, on_delete=models.CASCADE)
    monday_operating_hour_1_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    monday_operating_hour_1_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    monday_operating_hour_2_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    monday_operating_hour_2_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    tuesday_operating_hour_1_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    tuesday_operating_hour_1_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    tuesday_operating_hour_2_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    tuesday_operating_hour_2_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    wednesday_operating_hour_1_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    wednesday_operating_hour_1_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    wednesday_operating_hour_2_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    wednesday_operating_hour_2_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    thursday_operating_hour_1_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    thursday_operating_hour_1_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    thursday_operating_hour_2_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    thursday_operating_hour_2_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    friday_operating_hour_1_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    friday_operating_hour_1_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    friday_operating_hour_2_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    friday_operating_hour_2_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    saturday_operating_hour_1_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    saturday_operating_hour_1_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    saturday_operating_hour_2_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    saturday_operating_hour_2_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    sunday_operating_hour_1_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    sunday_operating_hour_1_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    sunday_operating_hour_2_start = models.CharField(
        max_length=8, choices=TIMES_CHOICES)
    sunday_operating_hour_2_end = models.CharField(
        max_length=8, choices=TIMES_CHOICES)

    def __str__(self):
        return ("Operating Hour Detail - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)


class HolidayDetail(models.Model):
    scenario = models.OneToOneField(Scenario, on_delete=models.CASCADE)
    holiday_period_1_start_date = models.IntegerField(null=True, blank=True)
    holiday_period_1_start_month = models.IntegerField(null=True, blank=True)
    holiday_period_1_end_date = models.IntegerField(null=True, blank=True)
    holiday_period_1_end_month = models.IntegerField(null=True, blank=True)
    holiday_period_2_start_date = models.IntegerField(null=True, blank=True)
    holiday_period_2_start_month = models.IntegerField(null=True, blank=True)
    holiday_period_2_end_date = models.IntegerField(null=True, blank=True)
    holiday_period_2_end_month = models.IntegerField(null=True, blank=True)
    holiday_period_3_start_date = models.IntegerField(null=True, blank=True)
    holiday_period_3_start_month = models.IntegerField(null=True, blank=True)
    holiday_period_3_end_date = models.IntegerField(null=True, blank=True)
    holiday_period_3_end_month = models.IntegerField(null=True, blank=True)
    holiday_period_4_start_date = models.IntegerField(null=True, blank=True)
    holiday_period_4_start_month = models.IntegerField(null=True, blank=True)
    holiday_period_4_end_date = models.IntegerField(null=True, blank=True)
    holiday_period_4_end_month = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return ("Holiday Details - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)

    
class PriceForecastOverride(models.Model):
    scenario = models.OneToOneField(Scenario, on_delete=models.CASCADE)
    year_2019 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2020 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2021 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2022 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2023 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2024 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2025 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2026 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
    year_2027 = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)
        

    def __str__(self):
        return ("Price Forecast Override - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)

class EscalationsOverride(models.Model):
    scenario = models.OneToOneField(Scenario, on_delete=models.CASCADE)
    month_1 = models.IntegerField(null=True, blank=True, choices=MONTH_2_CHOICES)
    year_1 = models.IntegerField(null=True, blank=True)
    override_1 = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    month_2 = models.IntegerField(null=True, blank=True, choices=MONTH_2_CHOICES)
    year_2 = models.IntegerField(null=True, blank=True)
    override_2 = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    month_3 = models.IntegerField(null=True, blank=True, choices=MONTH_2_CHOICES)
    year_3 = models.IntegerField(null=True, blank=True)
    override_3 = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    month_4 = models.IntegerField(null=True, blank=True, choices=MONTH_2_CHOICES)
    year_4 = models.IntegerField(null=True, blank=True)
    override_4 = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    month_5 = models.IntegerField(null=True, blank=True, choices=MONTH_2_CHOICES)
    year_5 = models.IntegerField(null=True, blank=True)
    override_5 = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    month_6 = models.IntegerField(null=True, blank=True, choices=MONTH_2_CHOICES)
    year_6 = models.IntegerField(null=True, blank=True)
    override_6 = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    
    def __str__(self):
        return ("Escalations Override - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)


class SolarExport(models.Model):
    scenario = models.OneToOneField(Scenario, on_delete=models.CASCADE)
    include_solar_export = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    year_2019 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2020 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2021 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2022 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2023 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2024 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2025 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2026 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2027 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2028 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2029 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2030 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    year_2031 = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    
    
    def __str__(self):
        return ("Solar Export - " + self.scenario.program_name.program_name + " / " + self.scenario.site_name.site_name + " / " + self.scenario.scenario_name)

    class Meta:
        ordering = ('id',)