from django.shortcuts import render, get_object_or_404
from .models import (CertificatePrices,  TariffEscalations, PeakEnergyRates,  OffpeakEnergyRates, LightingData, SolarData,
                     LedLight, ExistingLight, SolarCost, PFCCost, PostcodeResource)
from .serializers import (CertificatePricesSerializer, TariffEscalationsSerializer,
                         PeakEnergyRatesSerializer, OffpeakEnergyRatesSerializer,
                         LedLightSerializer,  ExistingLightSerializer, SolarCostSerializer,
                         PFCCostSerializer)
from .forms import PFCCostForm, SolarCostForm, SolarDataForm
from django.http import JsonResponse, HttpResponse
import json
import pandas as pd
from PAT.settings import BASE_DIR
import os
from decimal import Decimal
from PAT.settings import MEDIA_ROOT



# --------------------------General helper functions for views -------------------
def nullValidation(val):
    if val == "None" or val == "":
        return None
    return val



# ------------------------------- Ajax Views ---------------------------------------


# ------------------------------- Postcode Resource Download Data ----------------------
def download_data_page(request):
    data = {}    
    file_name = "PAT resources.xlsx"
    file_path = os.path.join(os.path.dirname(BASE_DIR), file_name)
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            # print(df.head())
            df.fillna('', inplace=True)
            # print(df.head())
            data['data'] = df.to_json(orient='index')
            PostcodeResource.objects.all().delete()        
            # insert 
            for i in range(len(df.index)):
                postcode_instance = PostcodeResource()
                postcode_instance.postcode = df['Postcode'][i]
                postcode_instance.suburb = df['Locality'][i]
                postcode_instance.state = df['State 2'][i]
                postcode_instance.latitude = Decimal(df['Lat'][i])
                postcode_instance.longitude = Decimal(df['Long'][i])
                if df['Emissions Factor'][i]!="":
                    postcode_instance.emissions_factor = Decimal(df['Emissions Factor'][i])
                postcode_instance.stc_zone = df['STC Zone'][i]
                postcode_instance.rating = Decimal(df['Rating (CER)'][i])
                postcode_instance.pvsyst_generation_factor = Decimal(df['Generation factor'][i])
                postcode_instance.save()
                print(i)
            data['message'] = "Success"            

        except Exception as e:
            print(str(e)) 
            data['message'] = str(e)   
    else:
        data['message'] = "File not found"
    return HttpResponse(json.dumps(data))
    






# ------------------------------- Renewable Certificates Views --------------------------

def save_certificate_page(request):
    data = get_object_or_404(CertificatePrices, id=1)
    JSONobj = json.loads(request.POST['JSONobj'])
    data.STCprice = JSONobj['stcPrice']
    data.VEECprice = JSONobj['veecPrice']
    data.ESCprice = JSONobj['escPrice']
    data.LGCprice2019 = JSONobj['lgcPrice2019']
    data.LGCprice2020 = JSONobj['lgcPrice2020']
    data.LGCprice2021 = JSONobj['lgcPrice2021']
    data.LGCprice2022 = JSONobj['lgcPrice2022']
    data.LGCprice2023 = JSONobj['lgcPrice2023']
    data.LGCprice2024 = JSONobj['lgcPrice2024']
    data.LGCprice2025 = JSONobj['lgcPrice2025']
    data.LGCprice2026 = JSONobj['lgcPrice2026']
    data.LGCprice2027 = JSONobj['lgcPrice2027']
    data.LGCprice2028 = JSONobj['lgcPrice2028']
    data.LGCprice2029 = JSONobj['lgcPrice2029']
    data.LGCprice2030 = JSONobj['lgcPrice2030']

    JSONlist = list()
    # print(type(json.loads(JSONobj)))
    try:
        data.save()
        # return HttpResponse('true')
    except:
        return HttpResponse('Not able to save')

    ser = CertificatePricesSerializer(CertificatePrices.objects.all()[0])
    JSONlist.append(ser.data)
    JSONlist = json.dumps(JSONlist)

    return HttpResponse(JSONlist)


# ------------------------------- Energy Rates and Escalations Views --------------------------


def save_tariff_escalations_page(request):
    tariff_escalations_2019 = get_object_or_404(TariffEscalations, year=2019)
    tariff_escalations_2020 = get_object_or_404(TariffEscalations, year=2020)
    tariff_escalations_2021 = get_object_or_404(TariffEscalations, year=2021)
    tariff_escalations_2022 = get_object_or_404(TariffEscalations, year=2022)
    tariff_escalations_2023 = get_object_or_404(TariffEscalations, year=2023)
    tariff_escalations_2024 = get_object_or_404(TariffEscalations, year=2024)
    tariff_escalations_2025 = get_object_or_404(TariffEscalations, year=2025)
    tariff_escalations_2026 = get_object_or_404(TariffEscalations, year=2026)
    tariff_escalations_2027 = get_object_or_404(TariffEscalations, year=2027)

    JSONobj = json.loads(request.POST['JSONobj'])
    tariff_escalations_2019.queensland = JSONobj['qld2019']
    tariff_escalations_2019.new_south_wales = JSONobj['nsw2019']
    tariff_escalations_2019.victoria = JSONobj['vic2019']
    tariff_escalations_2019.south_australia = JSONobj['sa2019']
    tariff_escalations_2019.western_australia = JSONobj['wa2019']
    tariff_escalations_2019.australian_capital_territory = JSONobj['act2019']
    tariff_escalations_2019.tasmania = JSONobj['tas2019']
    tariff_escalations_2019.northern_territory = JSONobj['nt2019']
    tariff_escalations_2020.queensland = JSONobj['qld2020']
    tariff_escalations_2020.new_south_wales = JSONobj['nsw2020']
    tariff_escalations_2020.victoria = JSONobj['vic2020']
    tariff_escalations_2020.south_australia = JSONobj['sa2020']
    tariff_escalations_2020.western_australia = JSONobj['wa2020']
    tariff_escalations_2020.australian_capital_territory = JSONobj['act2020']
    tariff_escalations_2020.tasmania = JSONobj['tas2020']
    tariff_escalations_2020.northern_territory = JSONobj['nt2020']
    tariff_escalations_2021.queensland = JSONobj['qld2021']
    tariff_escalations_2021.new_south_wales = JSONobj['nsw2021']
    tariff_escalations_2021.victoria = JSONobj['vic2021']
    tariff_escalations_2021.south_australia = JSONobj['sa2021']
    tariff_escalations_2021.western_australia = JSONobj['wa2021']
    tariff_escalations_2021.australian_capital_territory = JSONobj['act2021']
    tariff_escalations_2021.tasmania = JSONobj['tas2021']
    tariff_escalations_2021.northern_territory = JSONobj['nt2021']
    tariff_escalations_2022.queensland = JSONobj['qld2022']
    tariff_escalations_2022.new_south_wales = JSONobj['nsw2022']
    tariff_escalations_2022.victoria = JSONobj['vic2022']
    tariff_escalations_2022.south_australia = JSONobj['sa2022']
    tariff_escalations_2022.western_australia = JSONobj['wa2022']
    tariff_escalations_2022.australian_capital_territory = JSONobj['act2022']
    tariff_escalations_2022.tasmania = JSONobj['tas2022']
    tariff_escalations_2022.northern_territory = JSONobj['nt2022']
    tariff_escalations_2023.queensland = JSONobj['qld2023']
    tariff_escalations_2023.new_south_wales = JSONobj['nsw2023']
    tariff_escalations_2023.victoria = JSONobj['vic2023']
    tariff_escalations_2023.south_australia = JSONobj['sa2023']
    tariff_escalations_2023.western_australia = JSONobj['wa2023']
    tariff_escalations_2023.australian_capital_territory = JSONobj['act2023']
    tariff_escalations_2023.tasmania = JSONobj['tas2023']
    tariff_escalations_2023.northern_territory = JSONobj['nt2023']
    tariff_escalations_2024.queensland = JSONobj['qld2024']
    tariff_escalations_2024.new_south_wales = JSONobj['nsw2024']
    tariff_escalations_2024.victoria = JSONobj['vic2024']
    tariff_escalations_2024.south_australia = JSONobj['sa2024']
    tariff_escalations_2024.western_australia = JSONobj['wa2024']
    tariff_escalations_2024.australian_capital_territory = JSONobj['act2024']
    tariff_escalations_2024.tasmania = JSONobj['tas2024']
    tariff_escalations_2024.northern_territory = JSONobj['nt2024']
    tariff_escalations_2025.queensland = JSONobj['qld2025']
    tariff_escalations_2025.new_south_wales = JSONobj['nsw2025']
    tariff_escalations_2025.victoria = JSONobj['vic2025']
    tariff_escalations_2025.south_australia = JSONobj['sa2025']
    tariff_escalations_2025.western_australia = JSONobj['wa2025']
    tariff_escalations_2025.australian_capital_territory = JSONobj['act2025']
    tariff_escalations_2025.tasmania = JSONobj['tas2025']
    tariff_escalations_2025.northern_territory = JSONobj['nt2025']
    tariff_escalations_2026.queensland = JSONobj['qld2026']
    tariff_escalations_2026.new_south_wales = JSONobj['nsw2026']
    tariff_escalations_2026.victoria = JSONobj['vic2026']
    tariff_escalations_2026.south_australia = JSONobj['sa2026']
    tariff_escalations_2026.western_australia = JSONobj['wa2026']
    tariff_escalations_2026.australian_capital_territory = JSONobj['act2026']
    tariff_escalations_2026.tasmania = JSONobj['tas2026']
    tariff_escalations_2026.northern_territory = JSONobj['nt2026']
    tariff_escalations_2027.queensland = JSONobj['qld2027']
    tariff_escalations_2027.new_south_wales = JSONobj['nsw2027']
    tariff_escalations_2027.victoria = JSONobj['vic2027']
    tariff_escalations_2027.south_australia = JSONobj['sa2027']
    tariff_escalations_2027.western_australia = JSONobj['wa2027']
    tariff_escalations_2027.australian_capital_territory = JSONobj['act2027']
    tariff_escalations_2027.tasmania = JSONobj['tas2027']
    tariff_escalations_2027.northern_territory = JSONobj['nt2027']

   # JSONlist = list()
   # print(type(json.loads(JSONobj)))
    try:
        tariff_escalations_2019.save()
        tariff_escalations_2020.save()
        tariff_escalations_2021.save()
        tariff_escalations_2022.save()
        tariff_escalations_2023.save()
        tariff_escalations_2024.save()
        tariff_escalations_2025.save()
        tariff_escalations_2026.save()
        tariff_escalations_2027.save()
        # return HttpResponse('true')
    except:
        return HttpResponse('Not able to save')

    tariff_escalations = TariffEscalations.objects.all()
    JSONlist = list()

    for te in tariff_escalations:
        ser = TariffEscalationsSerializer(te)
        JSONlist.append(ser.data)

    JSONlist = json.dumps(JSONlist)

    return HttpResponse(JSONlist)

def save_peak_energy_rates_page(request):
    peak_energy_rates_2020 = get_object_or_404(PeakEnergyRates, year=2020)
    peak_energy_rates_2021 = get_object_or_404(PeakEnergyRates, year=2021)
    peak_energy_rates_2022 = get_object_or_404(PeakEnergyRates, year=2022)

    JSONobj = json.loads(request.POST['JSONobj'])
    peak_energy_rates_2020.queensland = nullValidation(JSONobj['qld2020'])
    peak_energy_rates_2020.new_south_wales = nullValidation(JSONobj['nsw2020'])
    peak_energy_rates_2020.victoria = nullValidation(JSONobj['vic2020'])
    peak_energy_rates_2020.south_australia = nullValidation(JSONobj['sa2020'])
    peak_energy_rates_2020.western_australia = nullValidation(
        JSONobj['wa2020'])
    peak_energy_rates_2020.australian_capital_territory = nullValidation(
        JSONobj['act2020'])
    peak_energy_rates_2020.tasmania = nullValidation(JSONobj['tas2020'])
    peak_energy_rates_2020.northern_territory = nullValidation(
        JSONobj['nt2020'])
    peak_energy_rates_2021.queensland = nullValidation(JSONobj['qld2021'])
    peak_energy_rates_2021.new_south_wales = nullValidation(JSONobj['nsw2021'])
    peak_energy_rates_2021.victoria = nullValidation(JSONobj['vic2021'])
    peak_energy_rates_2021.south_australia = nullValidation(JSONobj['sa2021'])
    peak_energy_rates_2021.western_australia = nullValidation(
        JSONobj['wa2021'])
    peak_energy_rates_2021.australian_capital_territory = nullValidation(
        JSONobj['act2021'])
    peak_energy_rates_2021.tasmania = nullValidation(JSONobj['tas2021'])
    peak_energy_rates_2021.northern_territory = nullValidation(
        JSONobj['nt2021'])
    peak_energy_rates_2022.queensland = nullValidation(JSONobj['qld2022'])
    peak_energy_rates_2022.new_south_wales = nullValidation(JSONobj['nsw2022'])
    peak_energy_rates_2022.victoria = nullValidation(JSONobj['vic2022'])
    peak_energy_rates_2022.south_australia = nullValidation(JSONobj['sa2022'])
    peak_energy_rates_2022.western_australia = nullValidation(
        JSONobj['wa2022'])
    peak_energy_rates_2022.australian_capital_territory = nullValidation(
        JSONobj['act2022'])
    peak_energy_rates_2022.tasmania = nullValidation(JSONobj['tas2022'])
    peak_energy_rates_2022.northern_territory = nullValidation(
        JSONobj['nt2022'])

   # JSONlist = list()
   # print(type(json.loads(JSONobj)))
    try:
        peak_energy_rates_2020.save()
        peak_energy_rates_2021.save()
        peak_energy_rates_2022.save()

        # return HttpResponse('true')
    except:
        print(JSONobj['act2020'])
        print(type(JSONobj['act2020']))
        return HttpResponse('Error')

    peak_energy_rates = PeakEnergyRates.objects.all()
    JSONlist = list()

    for per in peak_energy_rates:
        ser = PeakEnergyRatesSerializer(per)
        JSONlist.append(ser.data)

    JSONlist = json.dumps(JSONlist)

    return HttpResponse(JSONlist)

def save_offpeak_energy_rates_page(request):
    offpeak_energy_rates_2020 = get_object_or_404(
        OffpeakEnergyRates, year=2020)
    offpeak_energy_rates_2021 = get_object_or_404(
        OffpeakEnergyRates, year=2021)
    offpeak_energy_rates_2022 = get_object_or_404(
        OffpeakEnergyRates, year=2022)

    JSONobj = json.loads(request.POST['JSONobj'])
    offpeak_energy_rates_2020.queensland = nullValidation(JSONobj['qld2020'])
    offpeak_energy_rates_2020.new_south_wales = nullValidation(
        JSONobj['nsw2020'])
    offpeak_energy_rates_2020.victoria = nullValidation(JSONobj['vic2020'])
    offpeak_energy_rates_2020.south_australia = nullValidation(
        JSONobj['sa2020'])
    offpeak_energy_rates_2020.western_australia = nullValidation(
        JSONobj['wa2020'])
    offpeak_energy_rates_2020.australian_capital_territory = nullValidation(
        JSONobj['act2020'])
    offpeak_energy_rates_2020.tasmania = nullValidation(JSONobj['tas2020'])
    offpeak_energy_rates_2020.northern_territory = nullValidation(
        JSONobj['nt2020'])
    offpeak_energy_rates_2021.queensland = nullValidation(JSONobj['qld2021'])
    offpeak_energy_rates_2021.new_south_wales = nullValidation(
        JSONobj['nsw2021'])
    offpeak_energy_rates_2021.victoria = nullValidation(JSONobj['vic2021'])
    offpeak_energy_rates_2021.south_australia = nullValidation(
        JSONobj['sa2021'])
    offpeak_energy_rates_2021.western_australia = nullValidation(
        JSONobj['wa2021'])
    offpeak_energy_rates_2021.australian_capital_territory = nullValidation(
        JSONobj['act2021'])
    offpeak_energy_rates_2021.tasmania = nullValidation(JSONobj['tas2021'])
    offpeak_energy_rates_2021.northern_territory = nullValidation(
        JSONobj['nt2021'])
    offpeak_energy_rates_2022.queensland = nullValidation(JSONobj['qld2022'])
    offpeak_energy_rates_2022.new_south_wales = nullValidation(
        JSONobj['nsw2022'])
    offpeak_energy_rates_2022.victoria = nullValidation(JSONobj['vic2022'])
    offpeak_energy_rates_2022.south_australia = nullValidation(
        JSONobj['sa2022'])
    offpeak_energy_rates_2022.western_australia = nullValidation(
        JSONobj['wa2022'])
    offpeak_energy_rates_2022.australian_capital_territory = nullValidation(
        JSONobj['act2022'])
    offpeak_energy_rates_2022.tasmania = nullValidation(JSONobj['tas2022'])
    offpeak_energy_rates_2022.northern_territory = nullValidation(
        JSONobj['nt2022'])

   # JSONlist = list()
   # print(type(json.loads(JSONobj)))
    try:
        offpeak_energy_rates_2020.save()
        offpeak_energy_rates_2021.save()
        offpeak_energy_rates_2022.save()

        # return HttpResponse('true')
    except:
        print(JSONobj['act2020'])
        print(type(JSONobj['act2020']))
        return HttpResponse('Error')

    offpeak_energy_rates = OffpeakEnergyRates.objects.all()
    JSONlist = list()

    for oer in offpeak_energy_rates:
        ser = OffpeakEnergyRatesSerializer(oer)
        JSONlist.append(ser.data)

    JSONlist = json.dumps(JSONlist)
    return HttpResponse(JSONlist)


# ------------------------------- Lighting Database Views ---------------------------------

def save_lighting_data_page(request):
    data = {}
    if request.is_ajax():
        print("Not Ajax")
        JSONobj = json.loads(request.POST['JSONobj'])
        lighting_verdia_fee = JSONobj['lightingVerdiaFee']
        lighting_data = LightingData.objects.all().first()
        if not lighting_data:
            lighting_data = LightingData()        
        try:
            lighting_data.verdia_fee = lighting_verdia_fee
            lighting_data.save()
            data['message'] = "Success"
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

# ----------------- LED Views -------------------------

def save_led_page(request):
    JSONobj = json.loads(request.POST['JSONobj'])
    led_id = JSONobj['ledId']

    if led_id == "":
        led = LedLight()

    else:
        led = get_object_or_404(LedLight, id=JSONobj['ledId'])

    led.name = nullValidation(JSONobj['ledName'])
    led.fitting_type = nullValidation(JSONobj['ledFittingType'])
    led.installation_type = nullValidation(JSONobj['ledInstallType'])
    led.system_power = nullValidation(JSONobj['ledSystemPower'])
    led.led_life = nullValidation(JSONobj['ledLife'])
    led.replacement_fitting_price = nullValidation(
        JSONobj['ledReplacementFittingPrice'])
    led.replacement_fittings_per_hour = nullValidation(
        JSONobj['ledReplacementFittingsPerHour'])

    try:
        led.save()
        message = "success"
        return HttpResponse(message)
    except Exception as e:
        return HttpResponse(str(e))

def delete_led_page(request):
    JSONobj = json.loads(request.POST['JSONobj'])

    try:
        led = get_object_or_404(LedLight, id=JSONobj['ledId'])
        led.delete()
        return HttpResponse('Deleted')
    except Exception as e:
        return HttpResponse(str(e))

def edit_led_page(request):
    JSONobj = json.loads(request.POST['JSONobj'])

    try:
        led = get_object_or_404(LedLight, id=JSONobj['ledId'])
        ser = LedLightSerializer(led)
        JSONlist = json.dumps(ser.data)
        return HttpResponse(JSONlist)
    except Exception as e:
        return HttpResponse(str(e))

def show_led_database_page(request):
    led_lights = LedLight.objects.all()
    JSONlist = list()

    for led in led_lights:
        ser = LedLightSerializer(led)
        JSONlist.append(ser.data)

    JSONlist = json.dumps(JSONlist)

    return HttpResponse(JSONlist)


# ----------------- Existing Lighting Views --------------------


def save_existing_page(request):
    JSONobj = json.loads(request.POST['JSONobj'])
    existing_id = JSONobj['existingId']

    if existing_id == "":
        existing = ExistingLight()

    else:
        existing = get_object_or_404(ExistingLight, id=JSONobj['existingId'])

    existing.name = nullValidation(JSONobj['existingName'])
    existing.other_names = nullValidation(JSONobj['existingOtherNames'])
    existing.led_light = get_object_or_404(
        LedLight, id=nullValidation(JSONobj['existingLedReplacement']))
    existing.fitting_type = nullValidation(JSONobj['existingFittingType'])
    existing.installation_type = nullValidation(JSONobj['existingInstallType'])
    existing.lamp_quantity = nullValidation(JSONobj['existingLampQuantity'])
    existing.lamp_wattage = nullValidation(JSONobj['existingLampWattage'])
    existing.system_power = nullValidation(JSONobj['existingSystemPower'])
    existing.lamp_life = nullValidation(JSONobj['existingLife'])
    existing.replacement_lamp_price = nullValidation(
        JSONobj['existingReplacementLampPrice'])
    existing.replacement_lamp_fittings_per_hour = nullValidation(
        JSONobj['existingReplacementLampFittingsPerHour'])
    existing.replacement_fitting_price = nullValidation(
        JSONobj['existingReplacementFittingPrice'])
    existing.replacement_fittings_per_hour = nullValidation(
        JSONobj['existingReplacementFittingsPerHour'])

    try:
        existing.save()
        message = "success"
        return HttpResponse(message)
    except Exception as e:
        return HttpResponse(str(e))

def delete_existing_page(request):
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        existing = get_object_or_404(ExistingLight, id=JSONobj['existingId'])
        existing.delete()
        return HttpResponse('Deleted')
    except Exception as e:
        return HttpResponse(str(e))

def edit_existing_page(request):
    JSONobj = json.loads(request.POST['JSONobj'])

    try:
        existing = get_object_or_404(ExistingLight, id=JSONobj['existingId'])
        ser = ExistingLightSerializer(existing)
        JSONlist = json.dumps(ser.data)
        return HttpResponse(JSONlist)
    except Exception as e:
        return HttpResponse(str(e))

def show_existing_database_page(request):
    existing_lights = ExistingLight.objects.all()
    JSONlist = list()

    for existing in existing_lights:
        ser = ExistingLightSerializer(existing)
        JSONlist.append(ser.data)

    JSONlist = json.dumps(JSONlist)

    return HttpResponse(JSONlist)

def fill_existing_led_replacement_page(request):
    led_lights = LedLight.objects.all()
    JSONlist = list()

    for led in led_lights:
        ser = LedLightSerializer(led)
        JSONlist.append(ser.data)

    JSONlist = json.dumps(JSONlist)

    return HttpResponse(JSONlist)


# ------------------------------- Solar & PFC Cost Views ---------------------------------

# ---------------- Solar Cost Views ------------------

def show_solar_cost_page(request):
    data = {}
    try:
        solar_costs = SolarCost.objects.all()
        JSONlist = list()
        for solar_cost in solar_costs:
            ser = SolarCostSerializer(solar_cost)
            JSONlist.append(ser.data)
        
        data['value'] = JSONlist
        data['message'] = 'Success'
    except Exception as e:
        data['message'] = str(e)

    return HttpResponse(json.dumps(data))

def save_solar_cost_page(request):    
    data = {}
    if request.is_ajax():
        solar_cost_id = request.POST['solarCostId']
        if solar_cost_id == "":
            form = SolarCostForm(request.POST)
        else:
            solar_cost = get_object_or_404(SolarCost, id=solar_cost_id)
            form = SolarCostForm(request.POST, instance=solar_cost)
        try:
            if form.is_valid():
                form.save()
                data['message'] = 'saved'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

def delete_solar_cost_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        solar_cost = get_object_or_404(SolarCost, id=JSONobj['solarCostId'])
        solar_cost.delete()
        data['message'] = 'Success'      
    except Exception as e:
        data['message'] = str(e)   
    return HttpResponse(json.dumps(data))

def edit_solar_cost_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        solar_cost = get_object_or_404(SolarCost, id=JSONobj['solarCostId'])
        ser = SolarCostSerializer(solar_cost)
        data['value'] = ser.data
        data['message'] = 'Success'
    except Exception as e:
        data['message'] = str(e)
    return HttpResponse(json.dumps(data))


# ---------------- PFC Cost Views ------------------

def show_pfc_cost_page(request):
    data = {}
    try:
        pfc_costs = PFCCost.objects.all()
        JSONlist = list()
        for pfc_cost in pfc_costs:
            ser = PFCCostSerializer(pfc_cost)
            JSONlist.append(ser.data)
        
        data['value'] = JSONlist
        data['message'] = 'Success'
    except Exception as e:
        data['message'] = str(e)

    return HttpResponse(json.dumps(data))

def save_pfc_cost_page(request):
    data = {}
    if request.is_ajax():
        pfc_cost_id = request.POST['pfcCostId']
        if pfc_cost_id == "":
            form = PFCCostForm(request.POST)
        else:
            pfc_cost = get_object_or_404(PFCCost, id=pfc_cost_id)
            form = PFCCostForm(request.POST, instance=pfc_cost)
        try:
            if form.is_valid():
                form.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

def delete_pfc_cost_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        pfc_cost = get_object_or_404(PFCCost, id=JSONobj['pfcCostId'])
        pfc_cost.delete()
        data['message'] = 'Success'      
    except Exception as e:
        data['message'] = str(e)   
    return HttpResponse(json.dumps(data))

def edit_pfc_cost_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        pfc_cost = get_object_or_404(PFCCost, id=JSONobj['pfcCostId'])
        ser = PFCCostSerializer(pfc_cost)
        data['value'] = ser.data
        data['message'] = 'Success'
    except Exception as e:
        data['message'] = str(e)
    return HttpResponse(json.dumps(data))



# -------------------Solar Data Upload -----------------
def solar_data_upload_page(request):
    data = {}
    # print(request.POST)
    # print(request.FILES)
    if request.method == 'POST':
        form = SolarDataForm(request.POST, request.FILES)        
                
        if form.is_valid():            
            form_instance = form.save(commit=False)            
            # Check file extension 
            file_name = form_instance.file_name
            file_path = os.path.join(MEDIA_ROOT,'Solar Data',file_name) 
            if os.path.exists(file_path):
                 os.remove(file_path)   
            form_instance.file_name = file_name            
            form_instance.save()
            data['message'] = 'Success'
        else:
            print(form)
            data['message'] = 'Form did not save or is invalid'
    else:
        print(request.POST)
        print(request.FILES)
        data['message'] = 'Not post request'    
        
    return HttpResponse(json.dumps(data))




#---------------------------------Serializing 2 or more models ---------------------------------------
# def show_existing_database_page(request):
#     existing_lights = ExistingLight.objects.all()
#     led_lights = LedLight.objects.all()
#     JSONlist1 = list()
#     JSONlist2 = list()

#     for existing in existing_lights:
#         # ser = ExistingLightSerializer(existing)
#         ser = ExistingLightSerializer(existing)
#         JSONlist1.append(ser.data)

#     for led in led_lights:
#         # ser = ExistingLightSerializer(existing)
#         ser = LedLightSerializer(led)
#         JSONlist2.append(ser.data)

#     JSONlist = {
#         'existing_lights':JSONlist1,
#         'led_lights':JSONlist2,
#     }
#     JSONlist = json.dumps(JSONlist)

#     return HttpResponse(JSONlist)
