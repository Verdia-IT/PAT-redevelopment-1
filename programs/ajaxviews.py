from django.shortcuts import render, get_object_or_404
from .models import (Program, ProgramOutput, ProgramOverride)
from sites.models import Site
from .serializers import (ProgramSerializer, ProgramOutputSerializer)
from .forms import ProgramForm, ProgramOverrideForm
from django.http import JsonResponse, HttpResponse
import json
from simulations.algorithms import (arrange_interval_data, generate_lighting_interval_data,
                                    holiday_index_generator, add_solar_data, calculate_load_after_system,
                                    calculate_power_bill, calculate_load_summary, calculate_cashflow, calculate_capex_metrics,
                                    calculate_capex_metrics_iterations)

from simulations.algorithms import program_packager, program_manager
from scenarios.models import Scenario, IntervalData
from simulations.models import SimulationParameter
from lighting.models import LightingOutput
import pandas as pd
import numpy as np
import os
from PAT.settings import MEDIA_ROOT


# --------------------------General helper functions for views -------------------
def nullValidation(val):
    if val == "None" or val == "":
        return None
    return val



# ------------------------------- Ajax Views ---------------------------------------

def save_new_program_page(request):
    data = {}
    if request.is_ajax():
        program_id = request.POST['programId']
        if program_id == "":
            form = ProgramForm(request.POST)
        else:
            program = get_object_or_404(Program, id=program_id)
            form = ProgramForm(request.POST, instance=program)
        try:
            if form.is_valid():
                program = form.save()
                program_override = ProgramOverride.objects.filter(program=program)
                if not program_override:
                    program_override = ProgramOverride()
                    program_override.program = program
                    program_override.cashflow_start_month = 3
                    program_override.cashflow_start_year = 2021
                    program_override.discount_rate = 8
                    program_override.save()

                data['message'] = 'Success'                
            else:
                data['message'] = form.errors 
        except Exception as e:            
            data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def save_program_overrides_page(request):
    data = {}
    if request.is_ajax():
        program_id = request.POST['programId']
        program = get_object_or_404(Program, id=program_id)
        program_override = ProgramOverride.objects.filter(program=program)
        if program_override:
            if program_override.count() == 1:                
                form = ProgramOverrideForm(request.POST, instance=program_override.first())
                if form.is_valid():
                    form.save()
                    data['message'] = 'Success'
                else:
                    data['message'] = form.errors
        else:
            form = ProgramOverrideForm(request.POST)
            try:
                if form.is_valid():
                    program_override = form.save(commit=False)
                    program_override.program = program
                    program_override.save()                
                    data['message'] = 'Success'                
                else:
                    data['message'] = form.errors 
            except Exception as e:            
                data['message'] = str(e)     
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))



def show_programs_page(request):
    data = {}
    try:
        programs = Program.objects.all()
        JSONlist = list()
        for program in programs:
            ser = ProgramSerializer(program)
            JSONlist.append(ser.data)
        
        data['value'] = JSONlist
        data['message'] = 'Success'
    except Exception as e:
        data['message'] = str(e)

    return HttpResponse(json.dumps(data))


def run_simulations_page(request):
    data = {}
    
    if request.is_ajax():
        JSONobj = json.loads(request.POST['JSONobj'])
    else:
        data['message'] = "Not Ajax"
        return HttpResponse(json.dumps(data))

    try:
        program_id = JSONobj['programId']
        program_package_list, msg = program_packager(program_id)
        if msg != "Success":
            data['message'] = msg
            return HttpResponse(json.dumps(data))
        program_output_summary_list = program_manager(program_package_list)
        program_output_dict = program_output_summary_list[-1]
        
        #  Program Output
        program = Program.objects.filter(id=program_id).first()
        program_output = ProgramOutput.objects.filter(program=program)
        if program_output.count() == 0:
            program_output = ProgramOutput()
            program_output.program = program            
        else:
            program_output = program_output.first()
            

        program_output.solar_size = program_output_dict['program_output_summary_dict']['solar_size']      
        program_output.num_led = program_output_dict['program_output_summary_dict']['num_led_lights']
        program_output.pfc_size = program_output_dict['program_output_summary_dict']['pfc_size']
        program_output.num_sites = program_output_dict['program_output_summary_dict']['site_count']        
        program_output.savings_yr_1_dollar = program_output_dict['program_output_summary_dict']['net_savings_1st_year']
        program_output.savings_yr_1_energy = program_output_dict['program_output_summary_dict']['load_reduction']
        program_output.npv = program_output_dict['capex_metrics_dict']['NPV']
        program_output.irr = program_output_dict['capex_metrics_dict']['IRR']
        program_output.payback = program_output_dict['capex_metrics_dict']['payback']
        program_output.lcoe = program_output_dict['capex_metrics_dict']['LCOE']
        program_output.base_load_kwh = program_output_dict['program_output_summary_dict']['load_consumption'] * 1000
        program_output.electricity_current_bill = program_output_dict['system_year_cashflow_dict']['electricity_bill_original'][0]
        print(program_output)
        program_output.save()
        data['Program_Output'] = ProgramOutputSerializer(program_output).data
        data['message'] = "Success"        

    except Exception as e:
        data['message'] = str(e)
        return HttpResponse(json.dumps(data))
    
    # Save file (only in case of program level analysis) 
    # with open('simulationprogramdata.json', 'w') as f:
    #     json.dump(program_package_list, f, separators=(',', ': '))

    return HttpResponse(json.dumps(data))


def run_simulations_page_1(request):
    data = {}
    solar_size = 0
    pfc_size = 0
    num_leds = 0
    total_data = {}
    total_data['scenario'] = []
    final_data_list = []

    if request.is_ajax():
        JSONobj = json.loads(request.POST['JSONobj'])
    else:
        data['message'] = "Not Ajax"
        return HttpResponse(json.dumps(data))
    
    try:
        program_id = JSONobj['programId']
        program = get_object_or_404(Program, id=program_id)
        sites = Site.objects.filter(program_name=program, included=True)
        site_count = 0
        for site in sites:            
            scenarios = Scenario.objects.filter(site_name=site, chosen=True)
            if scenarios.count() == 1:
                scenario = scenarios.first()                
                try:
                    scenario_id = scenario.id
                    import time
                    t0 = time.time()
                    df = arrange_interval_data(scenario_id)                    
                    print('Completed... -> arrange_interval_data')
                    df = holiday_index_generator(scenario_id, df)
                    print('Completed... -> holiday_index_generator')
                    df, lighting_dict = generate_lighting_interval_data(scenario_id, df)
                    print('Completed... -> generate_lighting_interval_data')
                    df, solar_dict = add_solar_data(scenario_id, df)
                    print('Completed... -> add_solar_data')              
                    df, load_summary_dict = calculate_load_after_system(scenario_id, df)
                    print('Completed... -> calculate_load_after_system')                  
                    df, df_monthly_bill_summary, monthly_tariff_summary = calculate_power_bill(scenario_id, df)
                    print('Completed... -> calculate_power_bill')
                    df_monthly_load_summary = calculate_load_summary(scenario_id, df)
                    print('Completed... -> calculate_load_summary')
                    df_monthly_cashflow, df_system_year_cashflow, df_calendar_year_cashflow = calculate_cashflow(scenario_id, df, df_monthly_bill_summary, df_monthly_load_summary )
                    print('Completed... -> calculate_cashflow')
                    capex_metrics = calculate_capex_metrics(scenario_id, df_system_year_cashflow)
                    print('Completed... -> calculate_capex_metrics')
                    print(df.head())
                    print(df.columns)
                    t1 = time.time()
                    print("time taken = ",round(t1-t0),"sec") 
                    # print(df_monthly_cashflow.columns)
                    site_count = site_count + 1
                    if site_count == 1:
                        df_total_monthly_cashflow = df_monthly_cashflow
                        df_total_monthly_cashflow.drop(['panel_performance','escalations','escalations_multiplier','LGC_price','Feed_in_rates','lighting_energy_savings_proportion','solarpfc_energy_savings_proportion', 'total_cummulative_loss'],axis=1,inplace=True)
                        system_cost_metrics = {}
                        system_cost_metrics['stc_discount'] = capex_metrics['stc_discount']
                        system_cost_metrics['lighting_cost'] = capex_metrics['lighting_cost']
                        system_cost_metrics['solar_cost'] = capex_metrics['solar_cost']
                        system_cost_metrics['pfc_cost'] = capex_metrics['pfc_cost']                                       
                    else:
                        # cols_to_add = ['site_load_before', 'site_load_after_lighting', 'site_load_after_slp','lighting_load_reduction', 'solar_generation_ideal',
                        #                 'solar_generation_utilised', 'solar_generation_spill', 'electricity_bill_original', 'electricity_bill_after_lighting',
                        #                 'electricity_bill_after_slp', 'lighting_bill_savings', 'lighting_volume_savings', 'lighting_demand_savings',
                        #                 'lighting_maintenance_savings', 'total_lighting_savings', 'solarpfc_bill_savings', 'solarpfc_volume_savings',
                        #                 'solarpfc_demand_savings', 'LGC_utilised', 'LGC_spill', 'feed_in_income', 'total_solarpfc_savings', 'total_bill_savings',
                        #                 'LGCs', 'total_savings', 'net_cashflows'] 
                        cols_to_add = list(df_total_monthly_cashflow.columns.values) 
                        cols_remain_same = ['date','calendar_month', 'calendar_year', 'system_month', 'system_year']
                        cols_to_add = [item for item in cols_to_add if item not in cols_remain_same]    
                        df_total_monthly_cashflow[cols_to_add] = df_total_monthly_cashflow[cols_to_add].add(df_monthly_cashflow[cols_to_add], fill_value=0)
                        # print(df_total_monthly_cashflow.head())
                        # df_total_monthly_cashflow.to_excel('Total Cashflow.xlsx')
                        system_cost_metrics['stc_discount'] += capex_metrics['stc_discount']
                        system_cost_metrics['lighting_cost'] += capex_metrics['lighting_cost']
                        system_cost_metrics['solar_cost'] += capex_metrics['solar_cost']
                        system_cost_metrics['pfc_cost'] += capex_metrics['pfc_cost']  

                    simulation_parameter = SimulationParameter.objects.filter(scenario=scenario).first()
                    solar_size += simulation_parameter.solar_size
                    pfc_size += simulation_parameter.pfc_size
                    if simulation_parameter.include_lighting == "Yes":
                        lighting_output = LightingOutput.objects.filter(scenario=scenario).first()
                        num_leds += lighting_output.number_of_lights              

                    # Combine all scenario data here for records -----------------------------------------------------------
                    simulation_parameter = SimulationParameter.objects.all().filter(
                        scenario=scenario).first()
                    # interval_data_id = simulation_parameter.interval_data.id
                    # interval_data = IntervalData.objects.all().filter(id=interval_data_id).first()
                    # file_path = os.path.join(
                    #     MEDIA_ROOT, 'Interval Data', interval_data.file_name)

                    # df = pd.read_csv(file_path)
                    scenario_data = {}
                    scenario_data['interval_data'] = df.to_json()
                    scenario_data['id'] = scenario_id
                    json_dict = {}
                    json_dict['scenario'] = scenario_id
                    json_dict['Datetime'] = df['Datetime'].values.tolist()
                    json_dict['kW'] = df['kW'].values.tolist()
                    json_dict['kVA'] = df['kVA'].values.tolist()
                    print(df[['solar_kW','solar_kW_POE']].head())
                    json_dict['solar_kW'] = df['solar_kW'].values.tolist()
                    final_data_list.append(json_dict)


                    # ------------------------------------------------------------------------------------------------------


                except Exception as e:
                    data['message'] = f'Error: "{site.site_name}\'s" chosen scenario has following error message <br>' + str(e)
                    return HttpResponse(json.dumps(data))
            else:
                data['message'] = f'Error: "{site.site_name}" does not have any scenarios.'
                return HttpResponse(json.dumps(data)) 
        
        # with open('data.json', 'w') as f:
        #     json.dump(final_data_list, f, separators=(',', ': '))
        system_cost_metrics['total_cost'] = system_cost_metrics['lighting_cost'] + system_cost_metrics['solar_cost'] + capex_metrics['pfc_cost']   
        print(system_cost_metrics)
        df_total_system_year_cashflow = df_total_monthly_cashflow.groupby(['system_year']).sum()
        df_total_system_year_cashflow.drop(['calendar_month','system_month','calendar_year',],axis=1, inplace=True)                    
        df_total_system_year_cashflow = df_total_system_year_cashflow.astype('float64')

        net_cashflows = np.zeros(len(df_total_system_year_cashflow.index)+1,)
        cum_cashflows = np.zeros(len(df_total_system_year_cashflow.index)+1,)
        net_cashflows[0] = -system_cost_metrics['total_cost']
        cum_cashflows[0] = -system_cost_metrics['total_cost']
        Payback = 25
        for i in range(len(df_total_system_year_cashflow.index)):
            current_val = df_total_system_year_cashflow['net_cashflows'].values[i]
            net_cashflows[i+1] = current_val
            cum_cashflows[i+1] = cum_cashflows[i] + current_val
            if cum_cashflows[i+1]>=0 and cum_cashflows[i]<0:
                Payback = np.around(i - (cum_cashflows[i] / (cum_cashflows[i+1] - cum_cashflows[i])),2)

        LCOE_calcs = np.zeros((len(df_total_system_year_cashflow.index)+1,6))
        discount_rate = 0.08

        for i in range(len(df_total_system_year_cashflow.index)+1):
            if i==0:
                LCOE_calcs[i,0] = -system_cost_metrics['solar_cost']
                LCOE_calcs[i,1] = -system_cost_metrics['solar_cost']
                LCOE_calcs[i,2] = 0
            else:
                LCOE_calcs[i,0] = 0
                LCOE_calcs[i,1] = df_total_system_year_cashflow['LGCs'].values[i-1]
                LCOE_calcs[i,2] = (df_total_system_year_cashflow['solar_generation_utilised'] + df_total_system_year_cashflow['solar_generation_spill']).values[i-1]
            LCOE_calcs[i,3] = (1 + discount_rate)**i
            LCOE_calcs[i,4] = LCOE_calcs[i,1] / LCOE_calcs[i,3]
            LCOE_calcs[i,5] = LCOE_calcs[i,2] / LCOE_calcs[i,3]

        NPV = round(np.npv(discount_rate, net_cashflows[:21]),2)
        IRRs = round(np.irr(net_cashflows[:21]),4)
        print(IRRs)
        if np.isnan(IRRs):
            IRRs = 0.0
        
        LCOE = -round(sum(LCOE_calcs[0:21,4]) / sum(LCOE_calcs[0:21,5]),4)
        if np.isnan(LCOE):
            LCOE = 0.0

        Simplified_LCOE = -round(sum(LCOE_calcs[0:21,0]) / sum(LCOE_calcs[0:21,2]),4)
        if np.isnan(Simplified_LCOE):
            Simplified_LCOE = 0.0
        
        print(df_total_monthly_cashflow)
        print(f'NPV = {NPV}')
        print(f'IRR = {IRRs}')
        print(f'LCOE = {LCOE}')
        print(f'Simplified_LCOE = {Simplified_LCOE}')
        print(f'Payback = {Payback}')
        data['NPV'] = NPV
        data['IRRs'] = IRRs
        data['LCOE'] = LCOE
        data['Simplified_LCOE'] = Simplified_LCOE
        data['Payback'] = Payback

        program_output = ProgramOutput.objects.filter(program=program)
        if program_output.count() == 0:
            program_output = ProgramOutput()
            program_output.program = program
            
        else:
            program_output = program_output.first()
            

        program_output.solar_size = solar_size        
        program_output.num_led = num_leds
        program_output.pfc_size = pfc_size
        program_output.num_sites = site_count        
        program_output.savings_yr_1_dollar = df_total_system_year_cashflow['total_savings'][1]
        program_output.savings_yr_1_energy = df_total_system_year_cashflow['site_load_before'][1] - df_total_system_year_cashflow['site_load_after_slp'][1]
        program_output.npv = NPV
        program_output.irr = IRRs
        program_output.payback = Payback
        program_output.lcoe = LCOE
        program_output.base_load_kwh = df_total_system_year_cashflow['site_load_before'][1]
        program_output.electricity_current_bill = df_total_system_year_cashflow['electricity_bill_original'][1]
        print(program_output)
        program_output.save()

        JSONlist = list()
        ser = ProgramOutputSerializer(program_output)
        JSONlist.append(ser.data)
        ser = ProgramSerializer(program)
        JSONlist.append(ser.data)
        data['Program_Output'] = JSONlist

        
        


        data['message'] = "Success"
    except Exception as e:
        data['message'] = str(e)

    return HttpResponse(json.dumps(data))