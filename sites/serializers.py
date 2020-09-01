from rest_framework import serializers

class SiteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    site_name = serializers.CharField(max_length=50)
    program_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    program_name = serializers.StringRelatedField(many=False, read_only=True)
    NMI = serializers.CharField(max_length=13)
    street_address = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)  
    state = serializers.CharField(max_length=20)
    postcode = serializers.IntegerField() 
    DNSP = serializers.CharField(max_length=20)
    industry_type = serializers.CharField(max_length=40)
    default_solar_data = serializers.CharField(max_length=20)
    included = serializers.BooleanField()