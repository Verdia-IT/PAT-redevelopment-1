from rest_framework import serializers


class ProgramSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    program_name = serializers.CharField(max_length=50)
    salesforce_id = serializers.CharField(max_length=20)
    contact_name = serializers.CharField(max_length=100)
    contact_title = serializers.CharField(max_length=100)
    contact_email = serializers.EmailField(max_length=100)
    contact_phone = serializers.CharField(max_length=15)


class ProgramOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    solar_size = serializers.DecimalField(max_digits=10, decimal_places=3)
    num_led = serializers.IntegerField()
    pfc_size = serializers.IntegerField()
    num_sites = serializers.IntegerField()
    savings_yr_1_dollar = serializers.DecimalField(max_digits=20,decimal_places=2)
    savings_yr_1_energy = serializers.DecimalField(max_digits=20,decimal_places=3)
    npv = serializers.DecimalField(max_digits=10, decimal_places=2)
    irr = serializers.DecimalField(max_digits=6, decimal_places=4)
    payback = serializers.DecimalField(max_digits=4, decimal_places=2)
    lcoe = serializers.DecimalField(max_digits=5,decimal_places=4)
    base_load_kwh = serializers.DecimalField(max_digits=20,decimal_places=3)
    electricity_current_bill = serializers.DecimalField(max_digits=20,decimal_places=2)
