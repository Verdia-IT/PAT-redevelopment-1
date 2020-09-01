from django.shortcuts import render, get_object_or_404
from .models import Scenario, IntervalData
from programs.models import Program
from sites.models import Site
from .serializers import (ScenarioSerializer)
from .forms import ScenarioForm, IntervalDataForm
from .models import Scenario, IntervalData
from django.http import JsonResponse, HttpResponse
import json
from django.core.files.storage import FileSystemStorage
from PAT.settings import MEDIA_ROOT
import os
import pandas as pd
from simulations.models import SimulationParameter


# --------------------------General helper functions for views -------------------


# ------------------------------- Ajax Views ---------------------------------------

def save_new_scenario_page(request):
    data = {}
    if request.is_ajax(): 
        site_id = request.POST['siteId']
        program_id = request.POST['programId'] 
        scenario_id = request.POST['scenarioId']  
        program = get_object_or_404(Program, id=program_id) 
        site = get_object_or_404(Site, id=site_id)
        if scenario_id == "":               
            form = ScenarioForm(request.POST)
        else: 
            scenario =  get_object_or_404(Scenario,id=scenario_id)     
            form = ScenarioForm(request.POST, instance=scenario)
        
        if form.is_valid():
            try:
                scenario = form.save(commit=False)
                scenario.program_name = program
                scenario.site_name = site
                scenario.summary = ""
                num_scenarios = Scenario.objects.filter(site_name=site).count()
                if num_scenarios == 0:
                    scenario.chosen = True       
                scenario.save()            
                data['message'] = 'Success'
            except Exception as e:
                if str(e) == "UNIQUE constraint failed: scenarios_scenario.program_name_id, scenarios_scenario.site_name_id, scenarios_scenario.scenario_name" : 
                    data['message'] = "This Scenario name already exists for this site."
                else:
                    data['message'] = str(e)
        else:
            data['message'] = form.errors              
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def show_scenarios_page(request):
    data = {}
    if request.is_ajax(): 
        JSONobj = json.loads(request.POST['JSONobj'])       
        # program_id = JSONobj['programId']  
        # program = Program.objects.get(id=program_id)
        site_id = JSONobj['siteId'] 
        site = Site.objects.get(id=site_id)
        scenarios = Scenario.objects.all().filter(site_name=site)
        
        JSONlist = list()
        try:
            for scenario in scenarios:
                ser = ScenarioSerializer(scenario)
                JSONlist.append(ser.data)            
            data['value'] = JSONlist
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
        return HttpResponse(json.dumps(data))


def delete_scenario_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        scenario = get_object_or_404(Scenario, id=JSONobj['scenarioId'])
        scenario.delete()
        data['message'] = 'Success'      
    except Exception as e:
        data['message'] = str(e)   
    return HttpResponse(json.dumps(data))


def choose_scenario_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        scenario_id = int(JSONobj['scenarioId'])
        scenario = get_object_or_404(Scenario, id=scenario_id)
        site = scenario.site_name
        scenarios = Scenario.objects.all().filter(site_name=site)
        for scenario in scenarios:
            # print(f'scenario id: {type(scenario_id)}')
            if scenario.id == scenario_id:
                scenario.chosen = True
            else:
                scenario.chosen = False
            scenario.save()
        data['message'] = 'Success'
    except Exception as e:
        data['message'] = str(e)   
    return HttpResponse(json.dumps(data))



# def upload_page(request):
#     data = {}
#     if request.method == "POST":
#         print(request.FILES)
#         uploaded_file = request.FILES['csv']
#         print(uploaded_file.name)
#         print(uploaded_file.size)
#         # data['fileName'] = uploaded_file.name
#         # data['fileSize'] = uploaded_file.size
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name,uploaded_file)
#         url = fs.url(name)
#         data['url'] = url
#     return HttpResponse(json.dumps(data))



def file_list_page(request):
    data = {}
    if request.method == "POST":
        JSONobj = json.loads(request.POST['JSONobj'])
        scenario = get_object_or_404(Scenario,id=JSONobj['scenarioId'])
        interval_data_instances = IntervalData.objects.all().filter(scenario=scenario)
        id_list = list()
        url_list = list()
        file_name_list = list()
        for instance in interval_data_instances:
            id_list.append(instance.id)
            url_list.append(instance.interval_data_file.url)
            file_name_list.append(instance.file_name)

        data['idList'] = id_list   
        data['urlList'] = url_list   
        data['fileNameList'] = file_name_list        

    return HttpResponse(json.dumps(data))



def interval_data_upload_page(request):
    data = {}
    # print(request.POST)
    # print(request.FILES)
    if request.method == 'POST':
        JSONobj = json.loads(request.POST['JSONobj'])
        scenario = get_object_or_404(Scenario,id=JSONobj['scenarioId'])
        # uploaded_file = request.FILES['csv']
        form = IntervalDataForm(request.POST, request.FILES)        
        if form.is_valid():            
            form_instance = form.save(commit=False)
            loc = os.path.join(MEDIA_ROOT,'Interval Data')
            file_name = scenario.site_name.NMI + ".csv"    
            fileNotExist = 1            
            fileCounter = 0
            while fileNotExist:
                fileCounter = fileCounter + 1
                if os.path.exists(os.path.join(loc,file_name)):
                    file_name = scenario.site_name.NMI + "_" + str(fileCounter) + ".csv"                
                else:
                    fileNotExist = 0    
            form_instance.file_name = file_name
            form_instance.scenario = scenario
            form_instance.save()

            interval_data_instances = IntervalData.objects.all().filter(scenario=scenario)
            id_list = list()
            url_list = list()
            file_name_list = list()
            for instance in interval_data_instances:
                id_list.append(instance.id)
                url_list.append(instance.interval_data_file.url)
                file_name_list.append(instance.file_name)

            data['idList'] = id_list   
            data['urlList'] = url_list   
            data['fileNameList'] = file_name_list 
            data['message'] = 'Success'
        else:
            print(form)
            data['message'] = 'Form did not save or is invalid'
    else:
        print(request.POST)
        print(request.FILES)
        data['message'] = 'Not post request'    
        
    return HttpResponse(json.dumps(data))



def delete_interval_data_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    interval_data_id = JSONobj['intervalDataId']
    scenario_id = JSONobj['scenarioId']
    scenario = get_object_or_404(Scenario, id=scenario_id)
    simulation_parameter = SimulationParameter.objects.all().filter(scenario=scenario).first()
    

    if simulation_parameter:
        if simulation_parameter.interval_data.id == interval_data_id:
            data['message'] = "This file cannot be deleted as it is the file chosen in Simulation Parameters."
        else:
            try:
                interval_data = get_object_or_404(IntervalData, id=interval_data_id)
                interval_data.delete()
                file_path = os.path.join(MEDIA_ROOT,'Interval Data',interval_data.file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                interval_data_instances = IntervalData.objects.all().filter(scenario=scenario)
                id_list = list()
                url_list = list()
                file_name_list = list()
                for instance in interval_data_instances:
                    id_list.append(instance.id)
                    url_list.append(instance.interval_data_file.url)
                    file_name_list.append(instance.file_name)

                data['idList'] = id_list   
                data['urlList'] = url_list   
                data['fileNameList'] = file_name_list      
                data['message'] = 'Success'      
            except Exception as e:
                data['message'] = str(e)   
    return HttpResponse(json.dumps(data))

def graph_interval_data_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        interval_data_id = JSONobj['intervalDataId']
        interval_data = get_object_or_404(IntervalData, id=interval_data_id)
        file_path = os.path.join(MEDIA_ROOT,'Interval Data',interval_data.file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            data['data'] = df.to_json(orient='index')
            # data['data'] = df.to_json()
        data['message'] = 'Success'
    except Exception as e:
        data['message'] = str(e)   
    return HttpResponse(json.dumps(data))
        