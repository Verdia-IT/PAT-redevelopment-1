from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
from programs.models import Program
from sites.models import Site
from sites.forms import SiteForm
from scenarios.forms import ScenarioForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/")
def main_site_page(request):
    print(request.POST)

    site_instance = get_object_or_404(Site,id=request.POST['hidden_site_id'])
    program_instance = site_instance.program_name
    context = {
        'program' : program_instance, 
        'site' : site_instance,        
        'site_form' : SiteForm(instance=site_instance),
        'scenario_form' : ScenarioForm(),
    }
    return render(request, 'main_site.html',context)
