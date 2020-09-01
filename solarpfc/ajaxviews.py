from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
import os

from references.models import CertificatePrices, PostcodeResource, SolarCost, PFCCost
from scenarios.models import Scenario
from .models import SolarLayout, SolarPrice, PFCPrice
from .forms import SolarLayoutForm, SolarPriceForm, PFCPriceForm
from PAT.settings import MEDIA_ROOT

from simulations.models import SimulationParameter



# --------------------------------------ajax views --------------------------

def solar_price_calculation_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            #  Calculating Solar Size      
            simulation_parameter = SimulationParameter.objects.all().filter(scenario=scenario).first()
            if not simulation_parameter:
                data['solar_size'] = 0
            else:
                data['solar_size'] = float(simulation_parameter.solar_size)     
           
            
            # Calculating Solar Unit Cost
            solar_unit_cost = JSONobj['solarUnitCost']
            solar_unit_cost_override = JSONobj['solarUnitCostOverride']


            solar_costs = SolarCost.objects.all().order_by('system_size')
            for solar_cost in solar_costs:
                if data['solar_size'] <= float(solar_cost.system_size):
                    data['solar_unit_cost'] = float(solar_cost.multi_site_dollar_per_watt)
                    data['verdia_fee'] = float(solar_cost.multi_site_verdia_fee)
                    break


            if solar_unit_cost_override == "":
                data['solar_unit_cost_override'] = ""
            else:
                data['solar_unit_cost'] = float(solar_unit_cost_override)
                data['solar_unit_cost_override'] = float(solar_unit_cost_override)

            data['gross_system_cost'] = round(data['solar_size']*data['solar_unit_cost']*1000,2)

            other_adjustments_1 = JSONobj['otherAdjustments1']
            if other_adjustments_1 == "":
                data['other_adjustments_1'] = 0
            else:
                data['other_adjustments_1'] = float(other_adjustments_1)

            verdia_fee = JSONobj['verdiaFee']            
            if verdia_fee != "":
                data['verdia_fee'] = float(verdia_fee)
            
            data['verdia_fee_dollars'] = (data['gross_system_cost'] + data['other_adjustments_1'])*(data['verdia_fee'])/100

            other_adjustments_2 = JSONobj['otherAdjustments2']
            if other_adjustments_2 == "":
                data['other_adjustments_2'] = 0
            else:
                data['other_adjustments_2'] = float(other_adjustments_2)
            
            
            data['system_type_override'] = JSONobj['systemTypeOverride']
            if data['system_type_override'] == "":
                data['system_type_override'] = "No override"

            if data['solar_size'] > 100:
                system_type = "LGC"
            else:
                system_type = "STC"

            if data['system_type_override']=="LGC":
                data['system_type'] = data['system_type_override']
            else:
                data['system_type'] = system_type


            stc_deeming_period = JSONobj['stcDeemingPeriod']
            if stc_deeming_period == "":
                data['stc_deeming_period'] = 11 # to be calculated
            else:
                data['stc_deeming_period'] = int(stc_deeming_period)

            certificate_price = CertificatePrices.objects.all().first()
            stc_price = float(certificate_price.STCprice)            
            postcode = scenario.site_name.postcode
            postcode_resource = PostcodeResource.objects.all().filter(postcode=postcode).first()
            rating = float(postcode_resource.rating)            
            
            if data['system_type'] == "STC":
                data['stc_discount'] = round(data['solar_size']*data['stc_deeming_period']*stc_price*rating,2)
            else:
                data['stc_discount'] = 0
            
            data['system_cost'] = round(data['gross_system_cost'] + data['other_adjustments_1'] + data['verdia_fee_dollars'] + data['other_adjustments_2'] - data['stc_discount'],2)
            if data['solar_size'] == 0:
                data['system_unit_cost'] = 0
            else:
                data['system_unit_cost'] = round(data['system_cost'] / data['solar_size']/1000,2)
            data['maintenance_cost_per_annum'] = round(data['system_cost']*0.5/100,2)
            if JSONobj['includeSolarMaintenance'] == "":
                data['include_solar_maintenance'] = "No"
            else:
                data['include_solar_maintenance'] = JSONobj['includeSolarMaintenance']
            data['message'] = 'Success'
            print('Solar Size:', data['solar_size'] )
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))


def save_solar_price_page(request):
    data = {}
    if request.is_ajax():        
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        
        solar_price = SolarPrice.objects.all().filter(scenario=scenario).first()
        if not solar_price:
            form = SolarPriceForm(request.POST)
        else:
            form = SolarPriceForm(request.POST, instance=solar_price)       
        
        try:
            if form.is_valid():
                solar_price = form.save(commit=False)
                solar_price.scenario = scenario
                solar_price.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def solar_layout_upload_page(request):
    data = {}
    # print(request.POST)
    # print(request.FILES)
    if request.method == 'POST':
        JSONobj = json.loads(request.POST['JSONobj'])
        scenario = get_object_or_404(Scenario,id=JSONobj['scenarioId'])
        # uploaded_file = request.FILES['csv']
        solar_layout = SolarLayout.objects.all().filter(scenario=scenario).first()
        if not solar_layout:
            form = SolarLayoutForm(request.POST, request.FILES)        
        else:
            form = SolarLayoutForm(request.POST, request.FILES, instance = solar_layout)
        
        if form.is_valid():            
            form_instance = form.save(commit=False)            
            # Check file extension 
            file_name = scenario.site_name.NMI + ".jpg"   
            file_path = os.path.join(MEDIA_ROOT,'Solar Layout',file_name) 
            if os.path.exists(file_path):
                 os.remove(file_path)   
            form_instance.file_name = file_name
            form_instance.scenario = scenario
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


def pfc_price_calculation_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)

            # Calculating PFC Size
            
            simulation_parameter = SimulationParameter.objects.all().filter(scenario=scenario).first()
            if not simulation_parameter:
                data['pfc_size'] = 0
            else:
                data['pfc_size'] = float(simulation_parameter.pfc_size)
            
            # PFC Unit Cost

            pfc_costs = PFCCost.objects.all().order_by('pfc_rating')
            for pfc_cost in pfc_costs:
                if data['pfc_size'] <= float(pfc_cost.pfc_rating):
                    data['pfc_unit_cost'] = round(float(pfc_cost.pfc_dollar_per_kvar),2)
                    data['pfc_unit_cost_override'] = ""   
                    break                 
                        
           
            pfc_unit_cost_override = JSONobj['pfcUnitCostOverride']
            if pfc_unit_cost_override != "":
                data['pfc_unit_cost'] = round(float(pfc_unit_cost_override),2)
                data['pfc_unit_cost_override'] = round(float(pfc_unit_cost_override),2)
            
            data['gross_system_cost'] = round(data['pfc_size']*data['pfc_unit_cost'],2)
            
            verdia_fee = JSONobj['verdiaFee']

            if verdia_fee == "":
                data['verdia_fee'] = 15
            else:
                data['verdia_fee'] = float(verdia_fee)

            data['verdia_fee_dollars'] = round(data['verdia_fee']*data['gross_system_cost']/100,2)
            data['system_cost'] = round(data['gross_system_cost'] + data['verdia_fee_dollars'],2)
            if data['pfc_size'] == 0:
                data['system_unit_cost'] = 0
            else:
                data['system_unit_cost'] = round(data['system_cost'] / data['pfc_size'] ,2)
                      
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))


def save_pfc_price_page(request):
    data = {}
    if request.is_ajax():        
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        
        pfc_price = PFCPrice.objects.all().filter(scenario=scenario).first()
        if not pfc_price:
            form = PFCPriceForm(request.POST)
        else:
            form = PFCPriceForm(request.POST, instance=pfc_price)       
        
        try:
            if form.is_valid():
                pfc_price = form.save(commit=False)
                pfc_price.scenario = scenario
                pfc_price.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))