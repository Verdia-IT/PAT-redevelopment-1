from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
import os
import pandas as pd
import numpy as np

from scenarios.models import Scenario
from .models import SimulationParameter, SimulationOutput
from .forms import SimulationParameterForm
from simulations.algorithms import scenario_packager
from simulations.algorithms import simulation_manager, iterations_manager


def save_simulation_parameter_page(request):
    data = {}
    if request.is_ajax():
        JSONobj = json.loads(request.POST['JSONobj'])
        print(JSONobj)
        scenario_id = JSONobj['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        simulation_parameter = SimulationParameter.objects.all().filter(
            scenario=scenario).first()
        if not simulation_parameter:
            form = SimulationParameterForm(request.POST)
        else:
            form = SimulationParameterForm(
                request.POST, instance=simulation_parameter)
        print(form)

        if form.is_valid():
            try:
                simulation_parameter = form.save(commit=False)
                simulation_parameter.scenario = scenario
                simulation_parameter.save()
                data['message'] = 'Success'
            except Exception as e:
                data['message'] = str(e)
        else:
            data['message'] = form.errors
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def run_simulation_page(request):
    data = {}
    if request.is_ajax():
        try:
            JSONobj = json.loads(request.POST['JSONobj'])
            scenario_id = JSONobj['scenarioId']
            scenario = get_object_or_404(Scenario, id=scenario_id)

            import time
            t0 = time.time()
            scenario_input_dict = scenario_packager(scenario_id)
            scenario_output_dict = simulation_manager(scenario_input_dict)
            t1 = time.time()
            print("time taken = ",round(t1-t0),"sec")  

            simulation_output = SimulationOutput.objects.all().filter(scenario=scenario).first()
            if not simulation_output:
                simulation_output = SimulationOutput()
            
            simulation_output.scenario = scenario
            simulation_output.npv = scenario_output_dict['capex_metrics_dict']['NPV']
            simulation_output.irr = scenario_output_dict['capex_metrics_dict']['IRR']
            simulation_output.payback = scenario_output_dict['capex_metrics_dict']['payback']
            simulation_output.lcoe = scenario_output_dict['capex_metrics_dict']['LCOE']
            simulation_output.save()

            solar_size = float(scenario_input_dict['solar_price_dict']['solar_size'])
            lighting_boolean = scenario_input_dict['lighting_boolean']
            num_lights = scenario_input_dict['lighting_output_dict']['number_of_lights'] * lighting_boolean
            IRRs = scenario_output_dict['capex_metrics_dict']['IRR']
            payback = scenario_output_dict['capex_metrics_dict']['payback']

            summary_string = f'{round(solar_size)} kW, {num_lights} LEDs, {round(IRRs*100,1)}% IRR, {round(payback, 2)} years payback'    
            scenario.summary = summary_string
            scenario.save()

            print(summary_string)

            data['val'] = scenario_output_dict
            data['message'] = "Success"
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def run_iterations_page(request):
    data = {}
    if request.is_ajax():
        JSONobj = json.loads(request.POST['JSONobj'])
        scenario_id = JSONobj['scenarioId']
        min_solar = JSONobj['minSolar']
        steps = JSONobj['steps']
        max_solar = JSONobj['maxSolar']
        solar_sizes = np.arange(min_solar,max_solar,steps)
        if max_solar not in solar_sizes:
            solar_sizes = np.r_[solar_sizes,max_solar]
        
        try:            
            import time
            t0 = time.time()
            scenario_input_dict = scenario_packager(scenario_id)
            data_dict = iterations_manager(scenario_input_dict, solar_sizes)
            t1 = time.time()
            print("time taken = ",round(t1-t0),"sec")          
            
            data['data_dict'] = data_dict
            data['message'] = "Success"
        except Exception as e:
            data['message'] = str(e)
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))

# def run_simulation_page_1(request):
#     data = {}
#     if request.is_ajax():
#         JSONobj = json.loads(request.POST['JSONobj'])
#         scenario_id = JSONobj['scenarioId']
#         scenario = get_object_or_404(Scenario, id=scenario_id)

#         try:
#             import time
#             t0 = time.time()
#             df = arrange_interval_data(scenario_id)
#             print('Completed... -> arrange_interval_data')
#             df = holiday_index_generator(scenario_id, df)
#             print('Completed... -> holiday_index_generator')
#             df, lighting_dict = generate_lighting_interval_data(scenario_id, df)
#             print('Completed... -> generate_lighting_interval_data')
#             df, solar_dict = add_solar_data(scenario_id, df)
#             print('Completed... -> add_solar_data')              
#             df, load_summary_dict = calculate_load_after_system(scenario_id, df)
#             print('Completed... -> calculate_load_after_system')                  
#             df, df_monthly_bill_summary, monthly_tariff_summary = calculate_power_bill(scenario_id, df)
#             print('Completed... -> calculate_power_bill')
#             df_monthly_load_summary = calculate_load_summary(scenario_id, df)
#             print('Completed... -> calculate_load_summary')
#             df_monthly_cashflow, df_system_year_cashflow, df_calendar_year_cashflow = calculate_cashflow(scenario_id, df, df_monthly_bill_summary, df_monthly_load_summary )
#             print('Completed... -> calculate_cashflow')
#             capex_metrics = calculate_capex_metrics(scenario_id, df_system_year_cashflow)
#             print('Completed... -> calculate_capex_metrics')
#             t1 = time.time()
#             print("time taken = ",round(t1-t0),"sec")  

#             data['NPV'] = capex_metrics['NPV']
#             data['IRR'] = capex_metrics['IRR']
#             data['Payback'] = capex_metrics['payback']
#             data['LCOE'] = capex_metrics['LCOE']
#             data['Simplified_LCOE'] = capex_metrics['Simplified_LCOE']

#             # Outputs Summary
#             data['load_consumption'] = df_monthly_load_summary['original_kwhs'].sum() / 1000
#             data['load_after_system'] = df_monthly_load_summary['after_slp_kwhs'].sum() / 1000
#             data['load_reduction'] = data['load_consumption'] - data['load_after_system']
#             data['load_reduction_percent'] = (data['load_reduction'] / data['load_consumption'])*100
#             data['greenhouse_reduction'] = 165

#             data['num_led_lights'] = lighting_dict['num_led_lights']
#             data['solar_size'] = solar_dict['solar_size']
#             data['pfc_kvar'] = load_summary_dict['pfc_kvar']
#             data['lighting_cost'] = capex_metrics['lighting_cost']
#             data['solar_cost'] = capex_metrics['solar_cost']
#             data['stc_discount'] = capex_metrics['stc_discount']
#             data['pfc_cost'] = capex_metrics['pfc_cost']
#             data['total_cost'] = capex_metrics['total_cost']
#             data['verdia_lighting_fee_dollars'] = capex_metrics['verdia_lighting_fee_dollars']
#             data['verdia_solar_fee_dollars'] = capex_metrics['verdia_solar_fee_dollars']
#             data['verdia_pfc_fee_dollars'] = capex_metrics['verdia_pfc_fee_dollars']
#             data['total_verdia_fee_dollars'] = capex_metrics['total_verdia_fee_dollars']

#             data['bill_savings_1st_year'] = df_system_year_cashflow['total_bill_savings'][1]
#             data['LGCs_1st_year'] = df_system_year_cashflow['LGCs'][1]

#             data['lighting_maintenance_savings_1st_year'] = df_system_year_cashflow['lighting_maintenance_savings'][1]
            
#             data['feed_in_income_1st_year'] = df_system_year_cashflow['feed_in_income'][1]
#             data['net_savings_1st_year'] = df_system_year_cashflow['total_savings'][1]

#             data['electricity_current_bill'] = (df_monthly_bill_summary['original_volume_charges'] + df_monthly_bill_summary['original_demand_charges'] + df_monthly_bill_summary['fixed_charges']).sum()
#             data['electricity_bill_1st_year'] =  df_system_year_cashflow['electricity_bill_original'][1]
#             data['electricity_bill_after_system_1st_year'] =  df_system_year_cashflow['electricity_bill_after_slp'][1]
#             data['electricity_bill_reduction_percent_1st_year'] =  (data['electricity_bill_1st_year'] - data['electricity_bill_after_system_1st_year'])/data['electricity_bill_1st_year']
#             data['electricity_cost_reduction_percent_1st_year'] =  data['net_savings_1st_year']/data['electricity_bill_1st_year']

#             data['lighting_load_reduction_1st_year'] = df_system_year_cashflow['lighting_load_reduction'][1]
#             data['lighting_load_reduction_percent_1st_year'] = data['lighting_load_reduction_1st_year'] / (data['load_consumption']*1000)
#             data['lighting_bill_savings_1st_year'] = df_system_year_cashflow['lighting_bill_savings'][1]
#             data['lighting_total_savings_1st_year'] = df_system_year_cashflow['total_lighting_savings'][1]
#             if data['lighting_total_savings_1st_year'] == 0:
#                 data['lighting_simple_payback'] = 25
#             else:
#                 data['lighting_simple_payback'] = data['lighting_cost'] / data['lighting_total_savings_1st_year'] 

#             data['solar_generation_ideal_1st_year'] = df_system_year_cashflow['solar_generation_ideal'][1]
#             data['solar_generation_utilised_1st_year'] = df_system_year_cashflow['solar_generation_utilised'][1]
#             if data['solar_generation_ideal_1st_year'] == 0:
#                 data['solar_utilisation_percent'] = 1 
#             else:
#                 data['solar_utilisation_percent'] = data['solar_generation_utilised_1st_year'] / data['solar_generation_ideal_1st_year']
#             data['solar_load_reduction_1st_year'] = data['solar_generation_utilised_1st_year']
#             data['solar_load_reduction_percent_1st_year'] = data['solar_generation_utilised_1st_year'] / (data['load_consumption']*1000)
#             data['solar_exported_1st_year'] = df_system_year_cashflow['solar_generation_spill'][1]
#             data['solar_bill_savings_1st_year'] = df_system_year_cashflow['solarpfc_bill_savings'][1]
#             data['peak_power_factor_before'] = df_monthly_load_summary['after_lighting_kw'].mean() / df_monthly_load_summary['after_lighting_kva'].mean()
#             data['peak_power_factor_after'] = df_monthly_load_summary['after_slp_kw'].mean() / df_monthly_load_summary['after_slp_kva'].mean()
#             if df_system_year_cashflow['total_solarpfc_savings'][1] == 0:
#                 data['solarpfc_simple_payback'] = 25
#             else:
#                 data['solarpfc_simple_payback'] = (data['solar_cost'] + data['pfc_cost'])/df_system_year_cashflow['total_solarpfc_savings'][1]

#             data['blended_rate'] = data['electricity_current_bill']/(data['load_consumption']*1000)

#             if data['solar_generation_utilised_1st_year'] == 0:
#                 data['solarpfc_savings_rate'] = 0
#             else:
#                 data['solarpfc_savings_rate'] = data['solar_bill_savings_1st_year'] / data['solar_generation_utilised_1st_year']

#             if df_system_year_cashflow['lighting_bill_savings'][1] == 0:
#                 data['lighting_energy_savings_proportion'] = 1
#             else:
#                 data['lighting_energy_savings_proportion'] = df_system_year_cashflow['lighting_volume_savings'][1] / df_system_year_cashflow['lighting_bill_savings'][1]

#             if df_system_year_cashflow['solarpfc_bill_savings'][1] == 0:
#                 data['solarpfc_energy_savings_proportion'] = 1
#             else:
#                 data['solarpfc_energy_savings_proportion'] = df_system_year_cashflow['solarpfc_volume_savings'][1] / df_system_year_cashflow['solarpfc_bill_savings'][1]
            
#             if df_system_year_cashflow['total_bill_savings'][1] == 0:
#                 data['total_energy_savings_proportion'] = 1
#             else:
#                 data['total_energy_savings_proportion'] = (df_system_year_cashflow['lighting_volume_savings'][1] + df_system_year_cashflow['solarpfc_volume_savings'][1]) / df_system_year_cashflow['total_bill_savings'][1]
            
#             if data['solar_generation_utilised_1st_year'] == 0:
#                 data['solarpfc_energy_savings_rate'] = 0
#             else:
#                 data['solarpfc_energy_savings_rate'] = df_system_year_cashflow['solarpfc_volume_savings'][1] / data['solar_generation_utilised_1st_year']

#             data['value'] = df.to_json(orient='index')
#             data['system_year_cashflow'] = df_system_year_cashflow.to_json(orient='index')
#             data['monthly_bill_summary'] = df_monthly_bill_summary.to_json(orient='index')
#             data['monthly_bill_summary_sum'] = df_monthly_bill_summary.sum().to_json(orient='index')
#             data['monthly_bill_summary_average'] = df_monthly_bill_summary.mean().to_json(orient='index')
#             data['monthly_load_summary'] = df_monthly_load_summary.to_json(orient='index')
#             data['monthly_load_summary_sum'] = df_monthly_load_summary.sum().to_json(orient='index')
#             data['monthly_load_summary_average'] = df_monthly_load_summary.mean().to_json(orient='index')

#             simulation_output = SimulationOutput.objects.all().filter(scenario=scenario).first()
#             if not simulation_output:
#                 simulation_output = SimulationOutput()
            
#             simulation_output.scenario=scenario
#             simulation_output.npv=data['NPV']
#             simulation_output.irr=data['IRR']
#             simulation_output.payback=data['Payback']
#             simulation_output.lcoe=data['LCOE']
#             simulation_output.save()

#             scenario.summary = str(data['solar_size']) + " kW, " + str(data['num_led_lights']) + " LEDs, " + str(round(data['IRR']*100,1)) + " IRR, " + str(data['Payback']) + " years payback"
#             scenario.save()

#             data['message'] = "Success"
#         except Exception as e:
#             data['message'] = str(e)
#     else:
#         data['message'] = 'Not Ajax'
    
#     return HttpResponse(json.dumps(data))



