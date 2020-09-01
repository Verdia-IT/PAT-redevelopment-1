
from rest_framework import serializers


class CertificatePricesSerializer(serializers.Serializer):
    STCprice = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    VEECprice = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    ESCprice = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2019 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2020 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2021 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2022 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2023 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2024 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2025 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2026 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2027 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2028 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2029 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)
    LGCprice2030 = serializers.DecimalField(
        default=36.00, max_digits=6, decimal_places=2)


class TariffEscalationsSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    queensland = serializers.DecimalField(max_digits=4, decimal_places=3)
    new_south_wales = serializers.DecimalField(max_digits=4, decimal_places=3)
    victoria = serializers.DecimalField(max_digits=4, decimal_places=3)
    south_australia = serializers.DecimalField(max_digits=4, decimal_places=3)
    western_australia = serializers.DecimalField(
        max_digits=4, decimal_places=3)
    australian_capital_territory = serializers.DecimalField(
        max_digits=4, decimal_places=3)
    tasmania = serializers.DecimalField(max_digits=4, decimal_places=3)
    northern_territory = serializers.DecimalField(
        max_digits=4, decimal_places=3)


class PeakEnergyRatesSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    queensland = serializers.DecimalField(max_digits=4, decimal_places=2)
    new_south_wales = serializers.DecimalField(max_digits=4, decimal_places=2)
    victoria = serializers.DecimalField(max_digits=4, decimal_places=2)
    south_australia = serializers.DecimalField(max_digits=4, decimal_places=2)
    western_australia = serializers.DecimalField(
        max_digits=4, decimal_places=2)
    australian_capital_territory = serializers.DecimalField(
        max_digits=4, decimal_places=2)
    tasmania = serializers.DecimalField(max_digits=4, decimal_places=2)
    northern_territory = serializers.DecimalField(
        max_digits=4, decimal_places=2)


class OffpeakEnergyRatesSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    queensland = serializers.DecimalField(max_digits=4, decimal_places=2)
    new_south_wales = serializers.DecimalField(max_digits=4, decimal_places=2)
    victoria = serializers.DecimalField(max_digits=4, decimal_places=2)
    south_australia = serializers.DecimalField(max_digits=4, decimal_places=2)
    western_australia = serializers.DecimalField(
        max_digits=4, decimal_places=2)
    australian_capital_territory = serializers.DecimalField(
        max_digits=4, decimal_places=2)
    tasmania = serializers.DecimalField(max_digits=4, decimal_places=2)
    northern_territory = serializers.DecimalField(
        max_digits=4, decimal_places=2)


class LedLightSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=45)
    fitting_type = serializers.CharField(max_length=2)
    installation_type = serializers.CharField(max_length=2)
    system_power = serializers.DecimalField(max_digits=5, decimal_places=1)
    led_life = serializers.IntegerField()
    replacement_fitting_price = serializers.DecimalField(
        max_digits=7, decimal_places=2)
    replacement_fittings_per_hour = serializers.IntegerField()


class ExistingLightSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=45)
    led_light_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    led_light = serializers.StringRelatedField(many=False, read_only=True)
    other_names = serializers.CharField()
    fitting_type = serializers.CharField(max_length=2)
    installation_type = serializers.CharField(max_length=2)
    lamp_quantity = serializers.IntegerField()
    lamp_wattage = serializers.DecimalField(max_digits=5, decimal_places=1)
    system_power = serializers.DecimalField(max_digits=5, decimal_places=1)
    lamp_life = serializers.IntegerField()
    replacement_lamp_price = serializers.DecimalField(
        max_digits=7, decimal_places=2)
    replacement_lamp_fittings_per_hour = serializers.IntegerField()
    replacement_fitting_price = serializers.DecimalField(
        max_digits=7, decimal_places=2)
    replacement_fittings_per_hour = serializers.IntegerField()


class SolarCostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    system_size = serializers.IntegerField()
    single_site_dollar_per_watt = serializers.DecimalField(
        max_digits=5, decimal_places=3)
    single_site_verdia_fee = serializers.DecimalField(
        max_digits=5, decimal_places=3)
    multi_site_dollar_per_watt = serializers.DecimalField(
        max_digits=5, decimal_places=3)
    multi_site_verdia_fee = serializers.DecimalField(
        max_digits=5, decimal_places=3)

class PFCCostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    pfc_rating = serializers.IntegerField()
    pfc_dollar_per_kvar = serializers.DecimalField(
        max_digits=5, decimal_places=1)
    

class PostcodeResourceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    postcode = serializers.IntegerField()
    suburb = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=20)
    latitude = serializers.DecimalField(max_digits=11, decimal_places=8)
    longitude = serializers.DecimalField(max_digits=11, decimal_places=8)
    emissions_factor = serializers.DecimalField(max_digits=5, decimal_places=3)
    stc_zone = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=4, decimal_places=3)
    pvsyst_generation_factor = serializers.DecimalField(max_digits=5, decimal_places=4)
