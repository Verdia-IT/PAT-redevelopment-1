from rest_framework import serializers

class ScenarioSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    scenario_name = serializers.CharField(max_length=50)
    site_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    site_name = serializers.StringRelatedField(many=False, read_only=True)
    program_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    program_name = serializers.StringRelatedField(many=False, read_only=True)
    notes = serializers.CharField()  
    summary = serializers.CharField() 
    chosen = serializers.BooleanField()   