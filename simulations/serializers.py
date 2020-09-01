from rest_framework import serializers


class SimulationParameterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    scenario_name = serializers.StringRelatedField(many=False, read_only=True)
    interval_data = serializers.SlugRelatedField(many=False, read_only=True, slug_field='file_name')    
    include_lighting = serializers.CharField(max_length=5)
    solar_size = serializers.DecimalField(max_digits=10, decimal_places=3)
    pfc_size = serializers.DecimalField(max_digits=10,decimal_places=2)
    target_pf = serializers.DecimalField(max_digits=5,decimal_places=2)