from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json

from lighting.models import LightingHourDetail
from scenarios.models import Scenario
from lighting.serializers import LightingHourDetailSerializer
from references.models import ExistingLight, LedLight
from sites.models import INDUSTRY_TYPE_CHOICES
from references.models import PostcodeResource, CertificatePrices
import math


# ------------------------------ Other Functions ------------------------------------------------------------------------
def estimate_operating_hours(ser):
    print(ser.data['lighting_type'])
    operating_hours = 3360
    return operating_hours


def calculate_existing_lamp_replacement_cost(existing_luminaire_id, labour_per_hour):
    existing_light = get_object_or_404(ExistingLight, id=existing_luminaire_id)
    existing_lamp_replacement_cost = (float(existing_light.lamp_quantity*existing_light.replacement_lamp_price) + labour_per_hour/existing_light.replacement_lamp_fittings_per_hour)
    return existing_lamp_replacement_cost

def estimate_operations_type_factor(industry_type, state):
    switcher={
        'Agriculture': 0,
        'Mining': 0,
        'Manufacturing': 1.67 ,
        'Electricity, Gas and Water Supply': 0,
        'Construction': 0,
        'Wholesale Trade': 1.9,
        'Retail Trade': 1.9,
        'Accommodation, Cafes and Restaurants': 1.9,
        'Transport and Storage': 1.9,
        'Communication Services': 1,
        'Finance and Insurance': 1,
        'Property and Business Services': 1,
        'Government Administration and Defence': 1,
        'Education': 1,
        'Health and Community Services': 2,
        'Cultural and Recreational Services': 1,
        'Personal and Other Services': 1.9,
    }
    operations_type_factor = switcher.get(industry_type,"Invalid")
    if operations_type_factor == "Invalid":
        switcher2={
        'new_south_wales': 0.636,
        'victoria': 1.10,
        }
        operations_type_factor = switcher2.get(state,"Invalid")
    return operations_type_factor

# ----------------------------Ajax functions --------------------------------------------------------------------------

# def lighting_type_change_page(request):
#     data = {}
#     if request.is_ajax():          
#         try:
#             JSONobj = json.loads(request.POST['JSONobj'])
#             lighting_id = JSONobj['lightingType'] 
#             if lighting_id=="":
#                 operating_hours = ""
#             else:
#                 scenario_id =  JSONobj['scenarioId']                 
#                 scenario = get_object_or_404(Scenario, id=scenario_id)          
#                 lighting_hour_detail = LightingHourDetail.objects.all().filter(scenario=scenario, id=lighting_id).first()                           
#                 ser = LightingHourDetailSerializer(lighting_hour_detail)
#                 # JSONlist.append(ser.data)
#                 operating_hours = estimate_operating_hours(ser)  
#             # JSONlist = list()     
#             # JSONlist.append(operating_hours)   
#             data['operatingHours'] = operating_hours
#             data['message'] = 'Success'                
#         except Exception as e:
#             data['message'] = str(e)
#     else:
#         data['message'] = 'Not ajax'
#     return HttpResponse(json.dumps(data))

def existing_luminaire_change_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            existing_luminaire_id = JSONobj['existingLuminaire']            
            if existing_luminaire_id=="":
                suggested_power = ""
                suggested_replacement_luminaire = ""                
            else:                        
                existing_light = get_object_or_404(ExistingLight, id=existing_luminaire_id)
                suggested_power = float(existing_light.system_power)
                suggested_replacement_luminaire = existing_light.led_light.name                
            data['suggestedPower'] = suggested_power
            data['suggestedReplacementLuminaire'] = suggested_replacement_luminaire            
            data['message'] = 'Success'                
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'  
    return HttpResponse(json.dumps(data))

def replacement_luminaire_change_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            replacement_luminaire_id = JSONobj['replacementLuminaire']             
            if replacement_luminaire_id=="":
                suggested_replacement_power = ""         
            else:                         
                replacement_light = get_object_or_404(LedLight, id=replacement_luminaire_id)
                suggested_replacement_power = float(replacement_light.system_power)                   
            data['suggestedReplacementPower'] = suggested_replacement_power            
            data['message'] = 'Success'                
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax' 
    return HttpResponse(json.dumps(data))


def lighting_input_calculation_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id =  JSONobj['scenarioId']
            existing_luminaire_id = JSONobj['existingLuminaire'] 
            replacement_luminaire_id = JSONobj['replacementLuminaire']
            lighting_id = JSONobj['lightingType'] 
            num_existing_luminaire = float(JSONobj['numExistingLuminaire'])
            num_replacement_luminaire = float(JSONobj['numReplacementLuminaire'])             
            existing_luminaire_power = float(JSONobj['existingLuminairePower'])
            replacement_luminaire_power = float(JSONobj['replacementLuminairePower'])            


            if JSONobj['discountAdjustment']=="":
                discount_adjustment = 0
            else:
                discount_adjustment = float(JSONobj['discountAdjustment']) 


            scenario = get_object_or_404(Scenario, id=scenario_id)          
            existing_light = get_object_or_404(ExistingLight, id=existing_luminaire_id)   
            replacement_light = get_object_or_404(LedLight, id=replacement_luminaire_id)              
            lighting_hour_detail = LightingHourDetail.objects.all().filter(scenario=scenario, id=lighting_id).first()                           
            # power reduction                    
            data['powerReduction'] = round((num_existing_luminaire*existing_luminaire_power - num_replacement_luminaire*replacement_luminaire_power)/1000,2)
            ser = LightingHourDetailSerializer(lighting_hour_detail)                
            data['operatingHours'] = estimate_operating_hours(ser)  
            data['totalEstimatedSavingskWhs'] = round(data['operatingHours']*data['powerReduction'],2)
            postcode = scenario.site_name.postcode
            postcode_instance = PostcodeResource.objects.all().filter(postcode=postcode).first()
            certificate_price = CertificatePrices.objects.all().first()
            industry_type = scenario.site_name.industry_type
            # veec discount calculation
            if scenario.site_name.state == "victoria":
                if data['operatingHours'] <= 3000:
                    data['veecDiscount'] = 10*float(postcode_instance.emissions_factor)*(float(data['totalEstimatedSavingskWhs'])/1000)*float(certificate_price.VEECprice)
                else:
                    data['veecDiscount'] = 3000*10*(replacement_luminaire_power*num_replacement_luminaire/1000)*(float(certificate_price.VEECprice)*float(postcode_instance.emissions_factor)*estimate_operations_type_factor(industry_type,scenario.site_name.state)/1000)
            else:
                data['veecDiscount'] = 0
            
            data['veecDiscount'] = round(data['veecDiscount'],2)
            # esc discount calculation
            if scenario.site_name.state == "new_south_wales":
                if data['operatingHours'] > 2000:
                    data['escDiscount'] = 2000*5*(replacement_luminaire_power*num_replacement_luminaire/1000)*(float(postcode_instance.emissions_factor)/1000)*float(certificate_price.ESCprice)
                else:
                    data['escDiscount'] = 5*float(postcode_instance.emissions_factor)*(float(data['totalEstimatedSavingskWhs'])/1000)*float(certificate_price.ESCprice)
            else:
                data['escDiscount'] = 0

            data['escDiscount'] = round(data['escDiscount'],2)
            data['totalDiscount'] = round(data['veecDiscount'] + data['escDiscount'] + discount_adjustment,2)
            data['discountAdjustment'] = discount_adjustment            

            if JSONobj['dollarPerFixture'] != "":
                data['dollarPerFixture'] = float(JSONobj['dollarPerFixture'])
            else:
                data['dollarPerFixture'] = float(replacement_light.replacement_fitting_price)            
            
            if JSONobj['labourPerHour'] != "":
                data['labourPerHour'] = float(JSONobj['labourPerHour'])
            else:
                data['labourPerHour'] = 100

            if JSONobj['fixturesPerHour'] != "":
                data['fixturesPerHour'] = float(JSONobj['fixturesPerHour'])
            else:
                data['fixturesPerHour'] = float(replacement_light.replacement_fittings_per_hour)
            
            data['totalCost'] = round(num_replacement_luminaire*(data['dollarPerFixture'] + data['labourPerHour']/data['fixturesPerHour']),2)
            data['replacementLuminaireLife'] = int(math.ceil((replacement_light.led_life/data['operatingHours'])*12))
            data['existingLampReplacementCost'] = round(float(calculate_existing_lamp_replacement_cost(existing_luminaire_id,100))*float(num_existing_luminaire),2)
            data['existingLuminaireLife'] = int(math.ceil((existing_light.lamp_life/data['operatingHours'])*12))   

           
            if JSONobj['maintenanceSavings'] != "":
                data['maintenanceSavings'] = float(JSONobj['maintenanceSavings'])
            else:
                data['maintenanceSavings'] = round((data['existingLampReplacementCost']*12/data['existingLuminaireLife']),2) 

            data['message'] = 'Success'                
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax' 
    print(data) 
    return HttpResponse(json.dumps(data))