from django.shortcuts import render, get_object_or_404
from scenarios.models import Scenario
from .models import (EnergyCharge, DemandCharge, FixedCharge)
from .serializers import (EnergyChargeSerializer, DemandChargeSerializer, FixedChargeSerializer)
from .forms import EnergyChargeForm, DemandChargeForm, FixedChargeForm
from django.http import JsonResponse, HttpResponse
import json

# ------------------------------- Energy Charges ------------------------------------

def save_energy_charge_page(request):
    data = {}
    if request.is_ajax():
        energy_charge_id = request.POST['energyChargeId']
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        if energy_charge_id == "":
            form = EnergyChargeForm(request.POST)
        else:
            energy_charge = get_object_or_404(EnergyCharge, id=energy_charge_id)
            form = EnergyChargeForm(request.POST, instance=energy_charge)
        try:
            if form.is_valid():
                energy_charge = form.save(commit=False)
                energy_charge.scenario = scenario
                energy_charge.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

def show_energy_charges_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            energy_charges = EnergyCharge.objects.all().filter(scenario=scenario)
            JSONlist = list()
            for energy_charge in energy_charges:
                ser = EnergyChargeSerializer(energy_charge)
                JSONlist.append(ser.data)            
            data['value'] = JSONlist
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))

def delete_energy_charge_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            energy_charge_id = JSONobj['energyChargeId']    
            energy_charge = get_object_or_404(EnergyCharge, id=energy_charge_id)
            energy_charge.delete()
            data['message'] = 'Success'      
        except Exception as e:
            data['message'] = str(e) 
    else:
        data['message'] = 'Not ajax' 
    return HttpResponse(json.dumps(data))

def edit_energy_charge_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            energy_charge_id = JSONobj['energyChargeId']
            energy_charge = get_object_or_404(EnergyCharge, id=energy_charge_id)    
            ser = EnergyChargeSerializer(energy_charge)
            data['value'] = ser.data
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))

# ------------------------------- Demand Charges ------------------------------------

def save_demand_charge_page(request):
    data = {}
    if request.is_ajax():
        demand_charge_id = request.POST['demandChargeId']
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        if demand_charge_id == "":
            form = DemandChargeForm(request.POST)
        else:
            demand_charge = get_object_or_404(DemandCharge, id=demand_charge_id)
            form = DemandChargeForm(request.POST, instance=demand_charge)
        try:
            if form.is_valid():
                demand_charge = form.save(commit=False)
                demand_charge.scenario = scenario
                demand_charge.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

def show_demand_charges_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            demand_charges = DemandCharge.objects.all().filter(scenario=scenario)
            JSONlist = list()
            for demand_charge in demand_charges:
                ser = DemandChargeSerializer(demand_charge)
                JSONlist.append(ser.data)            
            data['value'] = JSONlist
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))

def delete_demand_charge_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            demand_charge_id = JSONobj['demandChargeId']    
            demand_charge = get_object_or_404(DemandCharge, id=demand_charge_id)
            demand_charge.delete()
            data['message'] = 'Success'      
        except Exception as e:
            data['message'] = str(e) 
    else:
        data['message'] = 'Not ajax' 
    return HttpResponse(json.dumps(data))

def edit_demand_charge_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            demand_charge_id = JSONobj['demandChargeId']
            demand_charge = get_object_or_404(DemandCharge, id=demand_charge_id)    
            ser = DemandChargeSerializer(demand_charge)
            data['value'] = ser.data
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))


# ------------------------------- Fixed Charges ------------------------------------

def save_fixed_charge_page(request):
    data = {}
    if request.is_ajax():
        fixed_charge_id = request.POST['fixedChargeId']
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        if fixed_charge_id == "":
            form = FixedChargeForm(request.POST)
        else:
            fixed_charge = get_object_or_404(FixedCharge, id=fixed_charge_id)
            form = FixedChargeForm(request.POST, instance=fixed_charge)
        try:
            if form.is_valid():
                fixed_charge = form.save(commit=False)
                fixed_charge.scenario = scenario
                fixed_charge.save()
                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

def show_fixed_charges_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)
            fixed_charges = FixedCharge.objects.all().filter(scenario=scenario)
            JSONlist = list()
            for fixed_charge in fixed_charges:
                ser = FixedChargeSerializer(fixed_charge)
                JSONlist.append(ser.data)            
            data['value'] = JSONlist
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))

def delete_fixed_charge_page(request):
    data = {}
    if request.is_ajax():          
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            fixed_charge_id = JSONobj['fixedChargeId']    
            fixed_charge = get_object_or_404(FixedCharge, id=fixed_charge_id)
            fixed_charge.delete()
            data['message'] = 'Success'      
        except Exception as e:
            data['message'] = str(e) 
    else:
        data['message'] = 'Not ajax' 
    return HttpResponse(json.dumps(data))

def edit_fixed_charge_page(request):
    data = {}
    if request.is_ajax():     
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            fixed_charge_id = JSONobj['fixedChargeId']
            fixed_charge = get_object_or_404(FixedCharge, id=fixed_charge_id)    
            ser = FixedChargeSerializer(fixed_charge)
            data['value'] = ser.data
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not ajax'
    return HttpResponse(json.dumps(data))