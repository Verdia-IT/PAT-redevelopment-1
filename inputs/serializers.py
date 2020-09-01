from rest_framework import serializers


class BillDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)
    number_of_bills = serializers.IntegerField()
    bill_month = serializers.CharField(max_length=10)
    bill_year_ = serializers.IntegerField()
    bill_days = serializers.IntegerField()
    electricity_retailer = serializers.CharField(max_length=30)
    kwhs_consumed = serializers.DecimalField(max_digits=10, decimal_places=3)


class OperatingHourDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)
    monday_operating_hour_1_start = serializers.CharField(
        max_length=8)
    monday_operating_hour_1_end = serializers.CharField(
        max_length=8)
    monday_operating_hour_2_start = serializers.CharField(
        max_length=8)
    monday_operating_hour_2_end = serializers.CharField(
        max_length=8)
    tuesday_operating_hour_1_start = serializers.CharField(
        max_length=8)
    tuesday_operating_hour_1_end = serializers.CharField(
        max_length=8)
    tuesday_operating_hour_2_start = serializers.CharField(
        max_length=8)
    tuesday_operating_hour_2_end = serializers.CharField(
        max_length=8)
    wednesday_operating_hour_1_start = serializers.CharField(
        max_length=8)
    wednesday_operating_hour_1_end = serializers.CharField(
        max_length=8)
    wednesday_operating_hour_2_start = serializers.CharField(
        max_length=8)
    wednesday_operating_hour_2_end = serializers.CharField(
        max_length=8)
    thursday_operating_hour_1_start = serializers.CharField(
        max_length=8)
    thursday_operating_hour_1_end = serializers.CharField(
        max_length=8)
    thursday_operating_hour_2_start = serializers.CharField(
        max_length=8)
    thursday_operating_hour_2_end = serializers.CharField(
        max_length=8)
    friday_operating_hour_1_start = serializers.CharField(
        max_length=8)
    friday_operating_hour_1_end = serializers.CharField(
        max_length=8)
    friday_operating_hour_2_start = serializers.CharField(
        max_length=8)
    friday_operating_hour_2_end = serializers.CharField(
        max_length=8)
    saturday_operating_hour_1_start = serializers.CharField(
        max_length=8)
    saturday_operating_hour_1_end = serializers.CharField(
        max_length=8)
    saturday_operating_hour_2_start = serializers.CharField(
        max_length=8)
    saturday_operating_hour_2_end = serializers.CharField(
        max_length=8)
    sunday_operating_hour_1_start = serializers.CharField(
        max_length=8)
    sunday_operating_hour_1_end = serializers.CharField(
        max_length=8)
    sunday_operating_hour_2_start = serializers.CharField(
        max_length=8)
    sunday_operating_hour_2_end = serializers.CharField(
        max_length=8)



class HolidayDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)  
    holiday_period_1_start_date = serializers.IntegerField()
    holiday_period_1_start_month = serializers.IntegerField()
    holiday_period_1_end_date = serializers.IntegerField()
    holiday_period_1_end_month = serializers.IntegerField()
    holiday_period_2_start_date = serializers.IntegerField()
    holiday_period_2_start_month = serializers.IntegerField()
    holiday_period_2_end_date = serializers.IntegerField()
    holiday_period_2_end_month = serializers.IntegerField()
    holiday_period_3_start_date = serializers.IntegerField()
    holiday_period_3_start_month = serializers.IntegerField()
    holiday_period_3_end_date = serializers.IntegerField()
    holiday_period_3_end_month = serializers.IntegerField()
    holiday_period_4_start_date = serializers.IntegerField()
    holiday_period_4_start_month = serializers.IntegerField()
    holiday_period_4_end_date = serializers.IntegerField()
    holiday_period_4_end_month = serializers.IntegerField()

class PriceForecastOverrideSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)  
    year_2019 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2020 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2021 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2022 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2023 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2024 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2025 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2026 = serializers.DecimalField(max_digits=5,decimal_places=2)
    year_2027 = serializers.DecimalField(max_digits=5,decimal_places=2)


class EscalationsOverrideSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)  
    month_1 = serializers.IntegerField()
    year_1 = serializers.IntegerField()
    override_1 = serializers.DecimalField(max_digits=5, decimal_places=2)
    month_2 = serializers.IntegerField()
    year_2 = serializers.IntegerField()
    override_2 = serializers.DecimalField(max_digits=5, decimal_places=2)
    month_3 = serializers.IntegerField()
    year_3 = serializers.IntegerField()
    override_3 = serializers.DecimalField(max_digits=5, decimal_places=2)
    month_4 = serializers.IntegerField()
    year_4 = serializers.IntegerField()
    override_4 = serializers.DecimalField(max_digits=5, decimal_places=2)
    month_5 = serializers.IntegerField()
    year_5 = serializers.IntegerField()
    override_5 = serializers.DecimalField(max_digits=5, decimal_places=2)
    month_6 = serializers.IntegerField()
    year_6 = serializers.IntegerField()
    override_6 = serializers.DecimalField(max_digits=5, decimal_places=2)

class SolarExportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)  
    include_solar_export = serializers.CharField(max_length=5)
    year_2019 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2020 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2021 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2022 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2023 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2024 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2025 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2026 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2027 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2028 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2029 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2030 = serializers.DecimalField(max_digits=5, decimal_places=4)
    year_2031 = serializers.DecimalField(max_digits=5, decimal_places=4)