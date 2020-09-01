from rest_framework import serializers


class EnergyChargeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)
    tariff_name = serializers.CharField(max_length=15)
    include = serializers.CharField(max_length=5)
    amount = serializers.DecimalField(max_digits=5, decimal_places=4)
    tariff_type = serializers.CharField(max_length=10)
    weekday_start_time = serializers.CharField(max_length=10)
    weekday_end_time = serializers.CharField(max_length=10)
    weekend_start_time = serializers.CharField(max_length=10)
    weekend_end_time = serializers.CharField(max_length=10)
    months = serializers.CharField(max_length=30)
    category = serializers.CharField(max_length=10)

class DemandChargeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)
    tariff_name = serializers.CharField(max_length=15)
    include = serializers.CharField(max_length=5)
    chargeable_power = serializers.DecimalField(max_digits=8,decimal_places=2)
    amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    tariff_type = serializers.CharField(max_length=15)
    weekday_start_time = serializers.CharField(max_length=10)
    weekday_end_time = serializers.CharField(max_length=10)
    weekend_start_time = serializers.CharField(max_length=10)
    weekend_end_time = serializers.CharField(max_length=10)
    chargeable_power_type = serializers.CharField(max_length=4)
    months = serializers.CharField(max_length=30)
    threshold = serializers.CharField(max_length=30)
    category = serializers.CharField(max_length=10)


class FixedChargeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)
    tariff_name = serializers.CharField(max_length=15)
    include = serializers.CharField(max_length=5)
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)
    frequency = serializers.CharField(max_length=15)
    category = serializers.CharField(max_length=10)