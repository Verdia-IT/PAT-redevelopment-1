from django.db import models

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


class Program(models.Model):
    program_name = models.CharField(max_length=50, unique=True)
    salesforce_id = models.CharField(
        max_length=20, blank=True, null=True, unique=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_title = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return str(self.program_name)
    
    class Meta:
        ordering = ('program_name',)


class ProgramOutput(models.Model):
    program = models.OneToOneField(Program, on_delete=models.CASCADE)
    solar_size = models.DecimalField(max_digits=10, decimal_places=3)
    num_led = models.IntegerField()
    pfc_size = models.IntegerField()
    num_sites = models.IntegerField()
    savings_yr_1_dollar = models.DecimalField(max_digits=20,decimal_places=2)
    savings_yr_1_energy = models.DecimalField(max_digits=20,decimal_places=3)
    npv = models.DecimalField(max_digits=10, decimal_places=2)
    irr = models.DecimalField(max_digits=6, decimal_places=4)
    payback = models.DecimalField(max_digits=4, decimal_places=2)
    lcoe = models.DecimalField(max_digits=5,decimal_places=4)
    base_load_kwh = models.DecimalField(max_digits=20,decimal_places=3)
    electricity_current_bill = models.DecimalField(max_digits=20,decimal_places=2)


    def __str__(self):
        return self.program.program_name
 

class ProgramOverride(models.Model):
    program = models.OneToOneField(Program, on_delete=models.CASCADE)
    cashflow_start_month = models.IntegerField(choices=MONTH_2_CHOICES)
    cashflow_start_year = models.IntegerField()
    discount_rate = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.program.program_name
