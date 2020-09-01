from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json

from scenarios.models import Scenario
from .models import LightingHourDetail, LightingInput, LightingOutput
from .forms import LightingHourDetailForm, LightingInputForm, LightingOutputForm
from .serializers import LightingHourDetailSerializer, LightingInputSerializer
from references.models import LightingData


# ------------------------------- Ajax Views ---------------------------------------

def save_lighting_hour_detail_page(request):
    data = {}
    if request.is_ajax():
        lighting_hour_detail_id = request.POST['lightingHourDetailId']
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        if lighting_hour_detail_id == "":
            form = LightingHourDetailForm(request.POST)
        else:
            lighting_hour_detail = get_object_or_404(LightingHourDetail, id=lighting_hour_detail_id)
            form = LightingHourDetailForm(request.POST, instance=lighting_hour_detail)
        try:
            if form.is_valid():
                lighting_hour_detail = form.save(commit=False)
                lighting_hour_detail.scenario = scenario
                lighting_hour_detail.save()

                lighting_hour_details = LightingHourDetail.objects.all().filter(scenario=scenario)
                id_list = list()                
                lighting_type_list = list()

                for lighting_hour_detail in lighting_hour_details:
                    id_list.append(lighting_hour_detail.id)                    
                    lighting_type_list.append(lighting_hour_detail.lighting_type)

                data['idList'] = id_list                   
                data['lightingTypeList'] = lighting_type_list 
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def show_lighting_hour_details_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            lighting_hour_details = LightingHourDetail.objects.all().filter(scenario=scenario)
            JSONlist = list()
            for lighting_hour_detail in lighting_hour_details:
                ser = LightingHourDetailSerializer(lighting_hour_detail)
                JSONlist.append(ser.data)            
            data['value'] = JSONlist
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))
    
def delete_lighting_hour_detail_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            lighting_hour_detail_id = JSONobj['lightingHourDetailId']    
            lighting_hour_detail = get_object_or_404(LightingHourDetail, id=lighting_hour_detail_id)
            lighting_hour_detail.delete()
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            lighting_hour_details = LightingHourDetail.objects.all().filter(scenario=scenario)
            id_list = list()                
            lighting_type_list = list()

            for lighting_hour_detail in lighting_hour_details:
                id_list.append(lighting_hour_detail.id)                    
                lighting_type_list.append(lighting_hour_detail.lighting_type)

            data['idList'] = id_list                   
            data['lightingTypeList'] = lighting_type_list 
            data['message'] = 'Success'      
        except Exception as e:
            data['message'] = str(e) 
    else:
        data['message'] = 'Not ajax' 
    return HttpResponse(json.dumps(data))

def edit_lighting_hour_detail_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            lighting_hour_detail_id = JSONobj['lightingHourDetailId']
            lighting_hour_detail = get_object_or_404(LightingHourDetail, id=lighting_hour_detail_id)    
            ser = LightingHourDetailSerializer(lighting_hour_detail)
            data['value'] = ser.data
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))


def save_lighting_input_page(request):
    data = {}
    if request.is_ajax():
        lighting_input_id = request.POST['lightingInputId']
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        if lighting_input_id == "":
            form = LightingInputForm(request.POST)
        else:
            lighting_input = get_object_or_404(LightingInput, id=lighting_input_id)
            form = LightingInputForm(request.POST, instance=lighting_input)
        try:
            if form.is_valid():
                lighting_input = form.save(commit=False)
                lighting_input.scenario = scenario
                lighting_input.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

def show_lighting_inputs_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            lighting_inputs = LightingInput.objects.all().filter(scenario=scenario)
            JSONlist = list()
            for lighting_input in lighting_inputs:
                ser = LightingInputSerializer(lighting_input)
                JSONlist.append(ser.data)            
            data['value'] = JSONlist
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))


def delete_lighting_input_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            lighting_input_id = JSONobj['lightingInputId']    
            lighting_input = get_object_or_404(LightingInput, id=lighting_input_id)
            lighting_input.delete()
            data['message'] = 'Success'      
        except Exception as e:
            data['message'] = str(e) 
    else:
        data['message'] = 'Not ajax' 
    return HttpResponse(json.dumps(data))

def edit_lighting_input_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            lighting_input_id = JSONobj['lightingInputId']
            lighting_input = get_object_or_404(LightingInput, id=lighting_input_id)    
            ser = LightingInputSerializer(lighting_input)
            data['value'] = ser.data
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))

def lighting_outputs_calculation_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            other_adjustments_1 = JSONobj['otherAdjustments1']
            if other_adjustments_1 != "":
                data['other_adjustments_1'] = float(other_adjustments_1)
            else:
                data['other_adjustments_1'] = 0  
            print(other_adjustments_1)      
            if JSONobj['verdiaFee'] == "":
                lighting_output = LightingOutput.objects.all().filter(scenario=scenario).first()
                if not lighting_output:
                    data['verdia_fee'] = float(LightingData.objects.all().first().verdia_fee)
                else:
                    data['verdia_fee'] = float(lighting_output.verdia_fee)
            else:
                data['verdia_fee'] = float(JSONobj['verdiaFee'])
            other_adjustments_2 = JSONobj['otherAdjustments2']
            if other_adjustments_2 != "":
                data['other_adjustments_2'] = float(other_adjustments_2)
            else:
                data['other_adjustments_2'] = 0 
            scenario = get_object_or_404(Scenario, id=scenario_id)
            lighting_inputs = LightingInput.objects.all().filter(scenario=scenario)
            data['num_lights'] = 0
            data['power_reduction'] = 0
            data['total_discounts'] = 0
            data['installation_cost'] = 0
            data['maintenance_savings'] = 0            
            for lighting_input in lighting_inputs:
                data['num_lights'] = data['num_lights'] + lighting_input.number_of_replaced_luminaire
                data['power_reduction'] = round(data['power_reduction'] + float(lighting_input.power_reduction),2)
                data['total_discounts'] = data['total_discounts'] + round(float(lighting_input.total_discount),2)
                data['installation_cost'] = data['installation_cost'] + round(float(lighting_input.total_cost),2)
                data['maintenance_savings'] = data['maintenance_savings'] + round(float(lighting_input.maintenance_savings),2)

            data['verdia_fee_dollars'] = round((data['verdia_fee']/100)*(data['installation_cost'] + data['other_adjustments_1']),2)            
            data['total_cost'] = round(data['installation_cost'] + data['other_adjustments_1'] + data['other_adjustments_2'] + data['verdia_fee_dollars'] - data['total_discounts'],2)
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))


def save_lighting_output_page(request):
    data = {}
    if request.is_ajax():        
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        
        lighting_output = LightingOutput.objects.all().filter(scenario=scenario).first()
        if not lighting_output:
            form = LightingOutputForm(request.POST)
        else:
            form = LightingOutputForm(request.POST, instance=lighting_output)       
        
        try:
            if form.is_valid():
                lighting_output = form.save(commit=False)
                lighting_output.scenario = scenario
                lighting_output.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))