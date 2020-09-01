from django.shortcuts import render, get_object_or_404
from .models import (Site)
from programs.models import Program
from scenarios.models import Scenario
from scenarios.serializers import (ScenarioSerializer)
from .serializers import (SiteSerializer)
from .forms import SiteForm
from django.http import JsonResponse, HttpResponse
import json


# --------------------------General helper functions for views -------------------


# ------------------------------- Ajax Views ---------------------------------------

def save_new_site_page(request):
    data = {}
    if request.is_ajax(): 
        site_id = request.POST['siteId']
        program_id = request.POST['programId']  
        program = get_object_or_404(Program, id=program_id) 
        if site_id == "":  
            form = SiteForm(request.POST)
        else:                
            site = get_object_or_404(Site, id=site_id) 
            form = SiteForm(request.POST, instance=site)
           
        if form.is_valid():
            try:
                site = form.save(commit=False)
                site.program_name = program 
                if site_id == "":
                    site.included = True
                site.save()            
                data['message'] = 'Success'
            except Exception as e:
                if str(e) == "UNIQUE constraint failed: sites_site.program_name_id, sites_site.site_name" : 
                    data['message'] = "This Site name already exists for this program."
                else:
                    data['message'] = str(e)
        else:
            data['message'] = form.errors              
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

def show_sites_page(request):
    data = {}
    if request.is_ajax(): 
        JSONobj = json.loads(request.POST['JSONobj'])       
        program_id = JSONobj['programId']  
        program = Program.objects.get(id=program_id)
        sites = Site.objects.all().filter(program_name=program)
        
        JSONlist_site = list()
        JSONlist_scenario = list()
        try:
            for site in sites:
                ser1 = SiteSerializer(site)
                JSONlist_site.append(ser1.data)
                scenarios = Scenario.objects.all().filter(site_name=site)
                if scenarios:
                    for scenario in scenarios:
                        ser2 = ScenarioSerializer(scenario)
                        JSONlist_scenario.append(ser2.data)


            data['site_value'] = JSONlist_site
            data['scenario_value'] = JSONlist_scenario
            data['message'] = 'Success'
        except Exception as e:
            data['message'] = str(e)
        return HttpResponse(json.dumps(data))
        
            
def delete_site_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        site = get_object_or_404(Site, id=JSONobj['siteId'])
        site.delete()
        data['message'] = 'Success'      
    except Exception as e:
        data['message'] = str(e)   
    return HttpResponse(json.dumps(data))


def include_site_page(request):
    data = {}
    JSONobj = json.loads(request.POST['JSONobj'])
    try:
        site = get_object_or_404(Site, id=JSONobj['siteId'])
        include = JSONobj['include']
        if include == "Yes":
            site.included = True
        else:
            site.included = False
        site.save()
        data['message'] = 'Success'      
    except Exception as e:
        data['message'] = str(e)   
    return HttpResponse(json.dumps(data))



    
        
        
    

    