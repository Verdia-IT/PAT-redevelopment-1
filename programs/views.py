from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
from .models import Program, ProgramOutput, ProgramOverride
from .forms import ProgramForm, ProgramOverrideForm
from sites.models import Site
from sites.forms import SiteForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import math

# Create your views here.

@login_required(login_url="/")
def programs_page(request):   
    programs = Program.objects.all().order_by('id')
    paginator = Paginator(programs, 5)
    try:
        page = min(int(request.GET.get('page','1')), paginator.num_pages)
    except:
        page = 1
    try:
        programs = paginator.get_page(page)
    except (EmptyPage, InvalidPage):
        programs = paginator.page(paginator.num_pages)
    
    num_page_display = 5
    current_loc = math.ceil(page/num_page_display)
    start_range = max(1,(current_loc-1)*num_page_display+1)
    end_range = min(max(5,current_loc*num_page_display + 1),paginator.num_pages+1)
    my_range = list(range(start_range,end_range))
    print(my_range)
    print(programs.object_list)
  

    context = {
        'program_form' : ProgramForm,
        'programs': programs,
        'my_range': my_range
    }
    return render(request, 'current_programs.html', context)

@login_required(login_url="/")
def main_program_page(request):
    # print(request.POST)
    program_id = request.POST['hidden_program_id']
    program_instance = get_object_or_404(Program,id=program_id)
    program_output = ProgramOutput.objects.filter(program=program_instance)
    program_output_dict = {}
    if program_output.count() == 1:
        program_output = program_output.first()
        program_output_dict = {
            'dollar_savings':f'${round(program_output.savings_yr_1_dollar):,}',
            'electricity_current_bill':f'${round(program_output.electricity_current_bill):,}',
            'energy_savings_percent':f'{round(program_output.savings_yr_1_energy*100/program_output.base_load_kwh)}',
            'savings_yr_1_energy':round(program_output.savings_yr_1_energy/1000),
            'base_load_mwh':round(program_output.base_load_kwh/1000),
            'npv':f'${round(program_output.npv):,}',
            'irr':program_output.irr*100,
            }
    
    program_overrides = ProgramOverride.objects.filter(program=program_instance)
    if program_overrides:
        if program_overrides.count() == 1:
            program_override = program_overrides.first()
            program_override_form = ProgramOverrideForm(instance=program_override)
    else:
        program_override_form = ProgramOverrideForm()


    context = {
        'program' : program_instance,
        'program_output' : program_output,
        'program_output_dict': program_output_dict,
        'program_form' : ProgramForm(instance=program_instance),
        'site_form' : SiteForm,
        'program_override_form': program_override_form,
    }
    return render(request, 'main_program.html',context)


