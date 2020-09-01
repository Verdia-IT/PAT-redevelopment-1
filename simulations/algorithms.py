from django.shortcuts import render, get_object_or_404
from references.models import TariffEscalations, CertificatePrices, SolarCost, PostcodeResource
from references.serializers import TariffEscalationsSerializer, CertificatePricesSerializer, SolarCostSerializer, PostcodeResourceSerializer
from sites.models import Site
from sites.serializers import SiteSerializer
from scenarios.models import Scenario, IntervalData
from scenarios.serializers import ScenarioSerializer
from simulations.models import SimulationParameter
from simulations.serializers import SimulationParameterSerializer
from solarpfc.models import SolarPrice, PFCPrice
from solarpfc.serializers import SolarPriceSerializer, PFCPriceSerializer
from lighting.models import LightingInput, LightingHourDetail, LightingOutput
from lighting.serializers import LightingOutputSerializer
from powerbillinputs.models import EnergyCharge, DemandCharge, FixedCharge
from powerbillinputs.serializers import EnergyChargeSerializer, DemandChargeSerializer, FixedChargeSerializer
from PAT.settings import MEDIA_ROOT
from inputs.models import HolidayDetail, PriceForecastOverride, EscalationsOverride, SolarExport
from inputs.serializers import HolidayDetailSerializer, SolarExportSerializer
# Serializers
from lighting.serializers import LightingHourDetailSerializer, LightingInputSerializer, LightingOutputSerializer

from programs.models import Program, ProgramOverride

import pandas as pd
import numpy as np
import os
import datetime as dt
import math
import json




def weekday_string(day):
    week_days = ["Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday", "Sunday"]
    return week_days[day]


def normaldist(mu, sigma, z):
    x = z*sigma + mu
    const = 1/(sigma*(math.sqrt(2*math.pi)))
    numerator = -(x-mu)**2
    denominator = 2*(sigma**2)
    p = const*(math.e**(numerator/denominator))
    return p


def dataframe_to_dict(df):
    """Converts dataframe to dict"""
    return_dict = {}
    for col in df.columns:
        return_dict[col] = df[col].values.tolist()
    
    return return_dict


# Packager functions ---------------------------------------------------------------------

def scenario_packager(scenario_id):
    """Package the scenario inputs in main dictionary"""
    input_data_dict = {} # main input dictionary

    # Fetch the scenario and check for errors
    scenarios = Scenario.objects.all().filter(id=scenario_id)   

    if scenarios.count() != 1:
        return "Error or Something"
    
    # current scenario
    scenario = scenarios.first()

    input_data_dict['scenario_data'] = ScenarioSerializer(scenario).data
    
    # Add Site data to input dict
    site_id = scenario.site_name.id
    sites = Site.objects.filter(id=site_id)
    if sites.count() != 1:
        return "Error or Something"

    site = sites.first()
    input_data_dict['site_data'] = SiteSerializer(site).data

    # Add simulation parameters to input dict
    simulation_parameters = SimulationParameter.objects.all().filter(scenario=scenario)
    try:
        simulation_parameter = simulation_parameters.first()
    except Exception as e:
        return str(e)
    
    simulation_parameter_dict = SimulationParameterSerializer(simulation_parameter)
    input_data_dict['simulation_parameter'] = simulation_parameter_dict.data

    # Add interval data to input dict
    try:
        interval_data = simulation_parameter.interval_data
        file_path = os.path.join(MEDIA_ROOT, 'Interval Data', interval_data.file_name)
    except Exception as e:
        return str(e)    

    interval_data_df = pd.read_csv(file_path)
    input_data_dict['interval_data_datetime'] = interval_data_df['Datetime'].values.tolist()
    input_data_dict['interval_data_kW'] = interval_data_df['kW'].values.tolist()
    input_data_dict['interval_data_kVA'] = interval_data_df['kVA'].values.tolist()

    # Add holiday details to input dict
    holiday_details = HolidayDetail.objects.all().filter(scenario=scenario)
    holiday_lists = []
    if holiday_details.count() == 1:
        holiday_detail = holiday_details.first()            
        for i in range(4):
            start_day = getattr(holiday_detail, "holiday_period_" + str(i+1) + "_start_date")
            start_month = getattr(holiday_detail, "holiday_period_" + str(i+1) + "_start_month")
            end_day = getattr(holiday_detail, "holiday_period_" + str(i+1) + "_end_date")
            end_month = getattr(holiday_detail, "holiday_period_" + str(i+1) + "_end_month")
            if start_day is not None:
                holiday_lists.append({'start_day':start_day, 'start_month':start_month, 'end_day':end_day, 'end_month':end_month} )             

    input_data_dict['holiday_lists'] = holiday_lists

    # inputs for generating lighting data
    if simulation_parameter.include_lighting == "Yes":
        lighting_boolean = 1
    else:
        lighting_boolean = 0

    lighting_hour_details = LightingHourDetail.objects.all().filter(scenario=scenario)
    lighting_hour_details_list = []
    if lighting_hour_details:
        for lighting_hour_detail in lighting_hour_details:
            ser = LightingHourDetailSerializer(lighting_hour_detail)
            lighting_hour_details_list.append(ser.data)

    lighting_inputs = LightingInput.objects.all().filter(scenario=scenario)
    lighting_inputs_list = []
    if lighting_inputs:
        for lighting_input in lighting_inputs:
            ser = LightingInputSerializer(lighting_input)
            lighting_inputs_list.append(ser.data)
        
    input_data_dict['lighting_boolean'] = lighting_boolean
    input_data_dict['lighting_hour_details_list'] = lighting_hour_details_list
    input_data_dict['lighting_inputs_list'] = lighting_inputs_list

    # inputs for add solar data
    solar_data = scenario.site_name.default_solar_data
    solar_data = solar_data + ".xlsx"
    file_path = os.path.join(MEDIA_ROOT, 'Solar Data', solar_data)
    # print(file_path)
    solar_df = pd.read_excel(file_path)
       
    input_data_dict['solar_data_datetime'] = solar_df['Datetime'].values.tolist()
    input_data_dict['solar_data_kW'] = solar_df['kW'].values.tolist()

    # Power Bill Calculation
    energy_charges_list = []
    energy_charges = EnergyCharge.objects.all().filter(scenario=scenario)
    if energy_charges.count() > 0:
        for energy_charge in energy_charges:
            ser = EnergyChargeSerializer(energy_charge)
            energy_charges_list.append(ser.data)
    
    demand_charges_list = []
    demand_charges = DemandCharge.objects.all().filter(scenario=scenario)
    if demand_charges.count() > 0:
        for demand_charge in demand_charges:
            ser = DemandChargeSerializer(demand_charge)
            demand_charges_list.append(ser.data)

    fixed_charges_list = []
    fixed_charges = FixedCharge.objects.all().filter(scenario=scenario)
    if fixed_charges.count() > 0:
        for fixed_charge in fixed_charges:
            ser = FixedChargeSerializer(fixed_charge)
            fixed_charges_list.append(ser.data)

    input_data_dict['energy_charges_list'] = energy_charges_list
    input_data_dict['demand_charges_list'] = demand_charges_list
    input_data_dict['fixed_charges_list'] = fixed_charges_list

    # Solar Costs to input dict
    solar_prices = SolarPrice.objects.all().filter(scenario=scenario)
    if solar_prices.count() != 1:
        return "Error! Solar Price Not found"    
    solar_price = solar_prices.first()
    input_data_dict['solar_price_dict'] = SolarPriceSerializer(solar_price).data
    system_type = solar_price.system_type
    if system_type == "STC":
        input_data_dict['lgc_flag'] = 0
    else:
        input_data_dict['lgc_flag'] = 1

    # PFC Costs to input dict
    pfc_prices = PFCPrice.objects.all().filter(scenario=scenario)
    if pfc_prices.count() != 1:
        return "Error! PFC Price Not found"    
    pfc_price = pfc_prices.first()
    input_data_dict['pfc_price_dict'] = PFCPriceSerializer(pfc_price).data

    # Lighting Costs
    lighting_output = LightingOutput.objects.all().filter(scenario=scenario)
    if lighting_output.count() != 1 and lighting_boolean == 1:
        return "Error! Lighting output does not exist"
    input_data_dict['lighting_output_dict'] = LightingOutputSerializer(lighting_output.first()).data
    
    
    # Hard coded variables to input dict        
    input_data_dict['panel_degradation'] = 0.5/100    
    input_data_dict['state'] = scenario.site_name.state
    
    
    # Tariff Escalations to input dict
    tariff_escalations_list = []
    for i in range(2019,2028):
        tariff_escalation = float(getattr(TariffEscalations.objects.filter(year=i).first(), input_data_dict['state'].lower()))
        tariff_escalations_list.append(tariff_escalation)
    
    input_data_dict['tariff_escalations_list'] = tariff_escalations_list

    # Price forecast override to input dict
    price_forecast_override = PriceForecastOverride.objects.all().filter(scenario=scenario).first()
    price_forecast_override_list = []
    if price_forecast_override:
        for i in range(2019,2028):
            temp_val = getattr(price_forecast_override, 'year_' + str(i))
            if temp_val:
                price_forecast_override_list.append(float(temp_val))
            else:
                price_forecast_override_list.append(temp_val)
    else:
        for i in range(9):
            price_forecast_override_list.append(None)
    
    input_data_dict['price_forecast_override_list'] = price_forecast_override_list

    # Escalations override to input dict
    escalations_override = EscalationsOverride.objects.all().filter(scenario=scenario).first()
    escalations_override_list = []
    for i in range(6):
        temp_dict = {}
        if escalations_override:            
            temp_dict['month_temp'] = getattr(escalations_override, 'month_' + str(i+1))
            temp_dict['year_temp'] = getattr(escalations_override, 'year_' + str(i+1))
            temp_dict['override_temp'] = getattr(escalations_override, 'override_' + str(i+1))
            if temp_dict['override_temp']:
                temp_dict['override_temp'] = float(temp_dict['override_temp'])
        else:
            temp_dict['month_temp'] = None
            temp_dict['year_temp'] = None
            temp_dict['override_temp'] = None

        escalations_override_list.append(temp_dict)

    input_data_dict['escalations_override_list'] = escalations_override_list

    # Solar export
    solar_exports = SolarExport.objects.all().filter(scenario=scenario)
    if solar_exports.count() != 1:
        return "Error! Solar Export Not found"
    solar_export = solar_exports.first()
    input_data_dict['solar_export_dict'] = SolarExportSerializer(solar_export).data
    input_data_dict['include_solar_export'] = 0
    if solar_export:
        if solar_export.include_solar_export == "Yes":
            input_data_dict['include_solar_export'] = 1  

    # References
    certificate_prices = CertificatePrices.objects.all().first()
    input_data_dict['certificate_prices_dict'] = CertificatePricesSerializer(certificate_prices).data
    solar_cost = SolarCost.objects.all()
    input_data_dict['solar_cost_dict'] = SolarCostSerializer(solar_cost, many=True).data
    postcode = input_data_dict['site_data']['postcode']
    postcode_resource = PostcodeResource.objects.all().filter(postcode=postcode).first()
    input_data_dict['postcode_resource_dict'] = PostcodeResourceSerializer(postcode_resource).data
    

    # Program Overrides dict
    program_overrides_dict = {}
    program = scenario.program_name
    program_overrides = ProgramOverride.objects.filter(program=program)
    if program_overrides:
        if program_overrides.count() == 1:
            program_overrides = program_overrides.first()
            program_overrides_dict['cashflow_start_month'] = int(program_overrides.cashflow_start_month)
            program_overrides_dict['cashflow_start_year'] = int(program_overrides.cashflow_start_year)
            program_overrides_dict['discount_rate'] = float(program_overrides.discount_rate)
    else:
        program_overrides_dict['cashflow_start_month'] = 3
        program_overrides_dict['cashflow_start_year'] = 2021
        program_overrides_dict['discount_rate'] = 8
    
    input_data_dict['program_overrides_dict'] = program_overrides_dict

    # Save file (only in case of program level analysis) 
    # with open('simulationdata.json', 'w') as f:
    #     json.dump(input_data_dict, f, separators=(',', ': '))            


    return input_data_dict


def program_packager(program_id):
    program_package_dict = {}
    site_list = []
    program = get_object_or_404(Program, id=program_id)
    sites = Site.objects.filter(program_name=program, included=True)
    for site in sites:            
        scenarios = Scenario.objects.filter(site_name=site, chosen=True)
        if scenarios.count() == 1:
            scenario = scenarios.first()              
            scenario_id = scenario.id
            scenario_package_dict = scenario_packager(scenario_id)
            site_list.append(scenario_package_dict)
        else:
            msg = f'Error: "{site.site_name}" does not have any scenarios.'
            return program_package_dict, msg

    program_package_dict['site_list'] = site_list
    # Program Overrides dict
    program_overrides_dict = {}
    program = scenario.program_name
    program_overrides = ProgramOverride.objects.filter(program=program)
    if program_overrides:
        if program_overrides.count() == 1:
            program_overrides = program_overrides.first()
            program_overrides_dict['cashflow_start_month'] = int(program_overrides.cashflow_start_month)
            program_overrides_dict['cashflow_start_year'] = int(program_overrides.cashflow_start_year)
            program_overrides_dict['discount_rate'] = float(program_overrides.discount_rate)
    else:
        program_overrides_dict['cashflow_start_month'] = 3
        program_overrides_dict['cashflow_start_year'] = 2021
        program_overrides_dict['discount_rate'] = 8
    
    program_package_dict['program_overrides_dict'] = program_overrides_dict

    msg = "Success"

    # with open('programinput.json', 'w') as f:
    #     json.dump(program_package_dict, f, separators=(',', ': '))

    return program_package_dict, msg

#  Manager Functions ----------------------------------------------------------------------

def simulation_manager(input_data_dict):
    # Initialize Main dataframe
    df_main = pd.DataFrame()
    
    # Arrange_interval_data    
    df_main = arrange_interval_data(df_main, input_data_dict)
    print("arrange_interval_data Completed.")
    
    # holiday_index_generator
    df_main = holiday_index_generator(df_main, input_data_dict)
    print("holiday_index_generator Completed.")

    # Lighting interval data
    df_main = generate_lighting_interval_data(df_main, input_data_dict)
    print("generate_lighting_interval_data Completed.")
    
    # Add Solar Data
    df_main = add_solar_data(df_main, input_data_dict)
    print("add_solar_data Completed.")
     
    # Load after system 
    df_main = calculate_load_after_system(df_main, input_data_dict)
    print("calculate_load_after_system Completed.")

    # power bill calculation
    df_main, df_monthly_bill_summary, df_monthly_tariff_summary =  calculate_power_bill(df_main, input_data_dict)
    print("calculate_power_bill Completed.")

    # load summary
    df_monthly_load_summary = calculate_load_summary(df_main)
    print("calculate_load_summary Completed.")
    

    # Cashflow   
    df_monthly_cashflow, df_system_year_cashflow, df_calendar_year_cashflow = calculate_cashflow(
                                                                    df=df_main,
                                                                    df_monthly_bill_summary=df_monthly_bill_summary,
                                                                    df_monthly_load_summary=df_monthly_load_summary,
                                                                    input_data_dict=input_data_dict
    ) 
                                                                    
    print("calculate_cashflow Completed.")

    # Capex metrics
    data = calculate_capex_metrics(df_system_year_cashflow, input_data_dict)
    print("calculate_capex_metrics Completed.")
        
    # Print commands
    # print(df_main.head())
    # print(df_monthly_bill_summary.head(12))
    # print(df_monthly_tariff_summary.head(12))
    # print(df_monthly_load_summary.head(12))  
    
    # return outputs in output_data_dict

    # Output Summary
    output_summary_dict = calculate_summary_params(df_monthly_load_summary, df_system_year_cashflow, df_monthly_bill_summary, input_data_dict)
    print("calculate_summary_params Completed.")

    output_data_dict = {}
    output_data_dict['data_analysis_dict'] = dataframe_to_dict(df_main)
    output_data_dict['monthly_bill_summary_dict'] = dataframe_to_dict(df_monthly_bill_summary)
    output_data_dict['monthly_bill_summary_sum_dict'] = df_monthly_bill_summary.sum().to_dict()
    output_data_dict['monthly_bill_summary_average_dict'] = df_monthly_bill_summary.mean().to_dict()
    output_data_dict['monthly_tariff_summary_dict'] = dataframe_to_dict(df_monthly_tariff_summary)
    output_data_dict['monthly_load_summary_dict'] = dataframe_to_dict(df_monthly_load_summary)
    output_data_dict['monthly_load_summary_sum_dict'] = df_monthly_load_summary.sum().to_dict()
    output_data_dict['monthly_load_summary_average_dict'] = df_monthly_load_summary.mean().to_dict()
    output_data_dict['monthly_cashflow_dict'] = dataframe_to_dict(df_monthly_cashflow)
    output_data_dict['system_year_cashflow_dict'] = dataframe_to_dict(df_system_year_cashflow)
    output_data_dict['calendar_year_cashflow_dict'] = dataframe_to_dict(df_calendar_year_cashflow)
    output_data_dict['capex_metrics_dict'] = data
    output_data_dict['output_summary_dict'] = output_summary_dict


    # data['monthly_bill_summary'] = df_monthly_bill_summary.to_json(orient='index')
    #         data['monthly_bill_summary_sum'] = df_monthly_bill_summary.sum().to_json(orient='index')
    #         data['monthly_bill_summary_average'] = df_monthly_bill_summary.mean().to_json(orient='index')
    #         data['monthly_load_summary'] = df_monthly_load_summary.to_json(orient='index')
    #         data['monthly_load_summary_sum'] = df_monthly_load_summary.sum().to_json(orient='index')
    #         data['monthly_load_summary_average'] = df_monthly_load_summary.mean().to_json(orient='index')
     
    # with open('simulationoutputdata.json', 'w') as f:
    #     json.dump(output_data_dict, f, separators=(',', ': '))

    return output_data_dict


def iterations_manager(input_data_dict, solar_sizes):
    # Initialize Main dataframe
    df_main = pd.DataFrame()
    
    # Arrange_interval_data    
    df_main = arrange_interval_data(df_main, input_data_dict)
    print("arrange_interval_data Completed.")
    
    # holiday_index_generator
    df_main = holiday_index_generator(df_main, input_data_dict)
    print("holiday_index_generator Completed.")

    # Lighting interval data
    df_main = generate_lighting_interval_data(df_main, input_data_dict)
    print("generate_lighting_interval_data Completed.")
    
    data = {}
    count = []
    solar_capex = []
    npvs = []
    paybacks = []
    irrs = []
    ten_year_savings = []
    lcoes = []
    solar_utilisations = []
    counter = 0

    for solar_size in solar_sizes:

        print(f'Solar Size: {solar_size} running...')
        # Add Solar Data
        df_main = add_solar_data_iterations(df_main, input_data_dict, solar_size)
        print("add_solar_data Completed.")
     
        # Load after system 
        df_main = calculate_load_after_system(df_main, input_data_dict)
        print("calculate_load_after_system Completed.")

        # power bill calculation
        df_main, df_monthly_bill_summary, df_monthly_tariff_summary =  calculate_power_bill(df_main, input_data_dict)
        print("calculate_power_bill Completed.")

        # load summary
        df_monthly_load_summary = calculate_load_summary(df_main)
        print("calculate_load_summary Completed.")
    

        # Cashflow   
        df_monthly_cashflow, df_system_year_cashflow, df_calendar_year_cashflow = calculate_cashflow(
                                                                        df=df_main,
                                                                        df_monthly_bill_summary=df_monthly_bill_summary,
                                                                        df_monthly_load_summary=df_monthly_load_summary,
                                                                        input_data_dict=input_data_dict
        ) 
                                                                    
        print("calculate_cashflow Completed.")

        # Capex metrics
        capex_metrics = calculate_capex_metrics_iterations(df_system_year_cashflow, input_data_dict, solar_size)
        print("calculate_capex_metrics Completed.")

        count.append(counter + 1)
        solar_capex.append(capex_metrics['solar_cost'])
        npvs.append(capex_metrics['NPV'])
        paybacks.append(capex_metrics['payback'])
        irrs.append(capex_metrics['IRR'])
        ten_year_savings.append(capex_metrics['ten_year_savings'])
        lcoes.append(capex_metrics['LCOE'])
        solar_utilisations.append(df_monthly_load_summary['solar_actual'].sum()/df_monthly_load_summary['solar_ideal'].sum())
        counter = counter + 1
        print(f'Solar Size: {solar_size} completed.')
    
    data['counters'] = count
    data['solar_sizes'] = solar_sizes.tolist()
    data['solar_capex'] = solar_capex
    data['npvs'] = npvs
    data['paybacks'] = paybacks
    data['irrs'] = irrs            
    data['ten_year_savings'] = ten_year_savings
    data['solar_utilisations'] = solar_utilisations
    data['lcoes'] = lcoes
    

    # Output Summary
    # output_summary_dict = calculate_summary_params(df_monthly_load_summary, df_system_year_cashflow, df_monthly_bill_summary, input_data_dict)
    # print("calculate_summary_params Completed.")

    # output_data_dict = {}
    # output_data_dict['data_analysis_dict'] = dataframe_to_dict(df_main)
    # output_data_dict['monthly_bill_summary_dict'] = dataframe_to_dict(df_monthly_bill_summary)
    # output_data_dict['monthly_bill_summary_sum_dict'] = df_monthly_bill_summary.sum().to_dict()
    # output_data_dict['monthly_bill_summary_average_dict'] = df_monthly_bill_summary.mean().to_dict()
    # output_data_dict['monthly_tariff_summary_dict'] = dataframe_to_dict(df_monthly_tariff_summary)
    # output_data_dict['monthly_load_summary_dict'] = dataframe_to_dict(df_monthly_load_summary)
    # output_data_dict['monthly_load_summary_sum_dict'] = df_monthly_load_summary.sum().to_dict()
    # output_data_dict['monthly_load_summary_average_dict'] = df_monthly_load_summary.mean().to_dict()
    # output_data_dict['monthly_cashflow_dict'] = dataframe_to_dict(df_monthly_cashflow)
    # output_data_dict['system_year_cashflow_dict'] = dataframe_to_dict(df_system_year_cashflow)
    # output_data_dict['calendar_year_cashflow_dict'] = dataframe_to_dict(df_calendar_year_cashflow)
    # output_data_dict['capex_metrics_dict'] = data
    # output_data_dict['output_summary_dict'] = output_summary_dict


    # data['monthly_bill_summary'] = df_monthly_bill_summary.to_json(orient='index')
    #         data['monthly_bill_summary_sum'] = df_monthly_bill_summary.sum().to_json(orient='index')
    #         data['monthly_bill_summary_average'] = df_monthly_bill_summary.mean().to_json(orient='index')
    #         data['monthly_load_summary'] = df_monthly_load_summary.to_json(orient='index')
    #         data['monthly_load_summary_sum'] = df_monthly_load_summary.sum().to_json(orient='index')
    #         data['monthly_load_summary_average'] = df_monthly_load_summary.mean().to_json(orient='index')
     
    # with open('simulationoutputdata.json', 'w') as f:
    #     json.dump(output_data_dict, f, separators=(',', ': '))

    return data


def program_manager(program_package_dict):
    program_package_list = program_package_dict['site_list']
    program_overrides_dict = program_package_dict['program_overrides_dict']

    """Program level analysis"""
    program_output_summary_list = []
    total_output_dict = {}
    program_output_summary_dict = {}

    for scenario_package_dict in program_package_list:
        output_summary_dict = simulation_manager(scenario_package_dict)
        program_output_summary_list.append(output_summary_dict)

    
    # Initialize variables for program output summary
    program_output_summary_dict['site_count'] = 0
    program_output_summary_dict['solar_size'] = 0
    program_output_summary_dict['pfc_size'] = 0
    program_output_summary_dict['lighting_cost'] = 0
    program_output_summary_dict['verdia_lighting_fee_dollars'] = 0
    program_output_summary_dict['num_led_lights'] = 0
    program_output_summary_dict['solar_cost'] = 0
    program_output_summary_dict['stc_discount'] = 0
    program_output_summary_dict['verdia_solar_fee_dollars'] = 0
    program_output_summary_dict['pfc_cost'] = 0
    program_output_summary_dict['verdia_pfc_fee_dollars'] = 0
    program_output_summary_dict['total_cost'] = 0
    program_output_summary_dict['total_verdia_fee_dollars'] = 0  
    

    # Cashflows and cost metrics
    site_count = 0
    for scenario_output_summary_dict in program_output_summary_list:
        site_count = site_count + 1
        df_monthly_cashflow = pd.DataFrame(scenario_output_summary_dict['monthly_cashflow_dict'])
        df_monthly_load_summary = pd.DataFrame(scenario_output_summary_dict['monthly_load_summary_dict'])
        
        if site_count == 1:
            # Cashflow
            df_total_monthly_cashflow = df_monthly_cashflow
            df_total_monthly_cashflow.drop(['panel_performance','escalations','escalations_multiplier',
                                            'LGC_price','Feed_in_rates','lighting_energy_savings_proportion',
                                            'solarpfc_energy_savings_proportion', 'total_cummulative_loss'],
                                            axis=1, inplace=True)

            # Load
            df_total_load_summary = df_monthly_load_summary
            df_total_load_summary.drop(['original_kw','original_kva','after_lighting_kw','after_lighting_kva',
                                        'after_slp_kw','after_slp_kva'], axis=1, inplace=True)


        else:
            # cashflow
            cols_to_add_cashflow = list(df_total_monthly_cashflow.columns.values) 
            cols_remain_same_cashflow = ['date','calendar_month', 'calendar_year', 'system_month', 'system_year']
            cols_to_add_cashflow = [item for item in cols_to_add_cashflow if item not in cols_remain_same_cashflow]    
            df_total_monthly_cashflow[cols_to_add_cashflow] = df_total_monthly_cashflow[cols_to_add_cashflow].add(df_monthly_cashflow[cols_to_add_cashflow], fill_value=0)

            # Load
            cols_to_add_load = list(df_total_load_summary.columns.values) 
            cols_remain_same_load = ['months']
            cols_to_add_load = [item for item in cols_to_add_load if item not in cols_remain_same_load]    
            df_total_load_summary[cols_to_add_load] = df_total_load_summary[cols_to_add_load].add(df_monthly_load_summary[cols_to_add_load], fill_value=0) 
        

        program_output_summary_dict['solar_size'] += scenario_output_summary_dict['output_summary_dict']['solar_size']
        program_output_summary_dict['pfc_size'] += scenario_output_summary_dict['output_summary_dict']['pfc_size']
        program_output_summary_dict['lighting_cost'] += scenario_output_summary_dict['output_summary_dict']['lighting_cost']
        program_output_summary_dict['verdia_lighting_fee_dollars'] += scenario_output_summary_dict['output_summary_dict']['verdia_lighting_fee_dollars']
        program_output_summary_dict['num_led_lights'] += scenario_output_summary_dict['output_summary_dict']['num_led_lights']
        program_output_summary_dict['solar_cost'] += scenario_output_summary_dict['output_summary_dict']['solar_cost']
        program_output_summary_dict['stc_discount'] += scenario_output_summary_dict['output_summary_dict']['stc_discount']
        program_output_summary_dict['verdia_solar_fee_dollars'] += scenario_output_summary_dict['output_summary_dict']['verdia_solar_fee_dollars']
        program_output_summary_dict['pfc_cost'] += scenario_output_summary_dict['output_summary_dict']['pfc_cost']
        program_output_summary_dict['verdia_pfc_fee_dollars'] += scenario_output_summary_dict['output_summary_dict']['verdia_pfc_fee_dollars']
        program_output_summary_dict['total_cost'] += scenario_output_summary_dict['output_summary_dict']['total_cost']
        program_output_summary_dict['total_verdia_fee_dollars'] += scenario_output_summary_dict['output_summary_dict']['total_verdia_fee_dollars']

    # program_output_summary_dict['total_cost'] = program_output_summary_dict['lighting_cost'] + program_output_summary_dict['solar_cost'] + program_output_summary_dict['pfc_cost']
    program_output_summary_dict['site_count'] = site_count
    program_output_summary_dict['discount_rate'] = program_overrides_dict['discount_rate']


    total_output_dict['monthly_cashflow_dict'] = dataframe_to_dict(df_total_monthly_cashflow)
    total_output_dict['monthly_load_summary_dict'] = dataframe_to_dict(df_total_load_summary)
    total_output_dict['monthly_load_summary_sum_dict'] = df_total_load_summary.sum().to_dict()
    total_output_dict['monthly_load_summary_average_dict'] = df_total_load_summary.mean().to_dict()
    
    df_total_system_year_cashflow = df_total_monthly_cashflow.groupby(['system_year']).sum()
    df_total_system_year_cashflow.drop(['calendar_month','system_month','calendar_year',],axis=1, inplace=True)                    
    df_total_system_year_cashflow = df_total_system_year_cashflow.astype('float64')
    total_output_dict['system_year_cashflow_dict'] = dataframe_to_dict(df_total_system_year_cashflow)

    df_total_calendar_year_cashflow = df_total_monthly_cashflow.groupby(['calendar_year']).sum()
    df_total_calendar_year_cashflow.drop(['calendar_month','system_month','system_year',],axis=1, inplace=True)                    
    df_total_calendar_year_cashflow = df_total_calendar_year_cashflow.astype('float64')
    total_output_dict['calendar_year_cashflow_dict'] = dataframe_to_dict(df_total_calendar_year_cashflow)

    # Capex Metrics function
    capex_metrics_dict = calculate_capex_metrics_program(df_total_system_year_cashflow, program_output_summary_dict)
    total_output_dict['capex_metrics_dict'] = capex_metrics_dict
    

    
    # Output Summary function
    program_output_summary_dict = calculate_summary_params_program(df_total_load_summary, df_total_system_year_cashflow, program_output_summary_dict)
    total_output_dict['program_output_summary_dict'] = program_output_summary_dict
    
    program_output_summary_list.append(total_output_dict)
    # with open('programoutput.json', 'w') as f:
    #     json.dump(program_output_summary_list, f, separators=(',', ': '))

       
    return program_output_summary_list

# Algorithm functions ------------------------------------------------------------

def arrange_interval_data(df, input_data_dict):
    """
    It takes pandas dataframe as input consisting of 3 fields - Datetime, kW, kVA
    It does the following:
    1. Break the datetime in year, month, day, hour and minutes
    2. Creates weekdays
    3. Creates Reference Date from 2001/01/01 00:30
    4. Removes 29th Feb
    5. Sort the interval data from January 1st
    6. returns a dataframe
    """
    df['Datetime'] = input_data_dict['interval_data_datetime']
    df['kW'] = input_data_dict['interval_data_kW']
    df['kVA'] = input_data_dict['interval_data_kVA']

    # Conversion of Excel date to pandas datetime
    df['real_date'] = pd.TimedeltaIndex(df['Datetime'], unit='d') + dt.datetime(1899, 12, 30)
    # rounding to nearest 30 minutes
    df['rounded_date'] = df['real_date'].dt.round('30min')
    # Offsetting -1 minute
    df['offset_date'] = df['rounded_date'] + pd.Timedelta('-1 min')
    # Extracting Year, Month, Day, Hour and Minute in different columns
    df['year'] = pd.DatetimeIndex(df['offset_date']).year
    df['month'] = pd.DatetimeIndex(df['offset_date']).month
    df['day'] = pd.DatetimeIndex(df['offset_date']).day
    df['hour'] = pd.DatetimeIndex(df['rounded_date']).hour
    df['minute'] = pd.DatetimeIndex(df['rounded_date']).minute
    # Combining hours and minutes
    df['hours'] = df['hour'] + df['minute']/60
    df.loc[(df['hours'] == 0), 'hours'] = 24

    # Creating new dataframe with duplicate dropping, 29th feb drop and sorting

    df1 = df.drop_duplicates(subset=['month', 'day', 'hour', 'minute'])
    df1 = df1.drop(df1[(df1['month'] == 2) & (df1['day'] == 29)].index)
    df1 = df1.sort_values(['month', 'day', 'hours', 'minute'], ascending=(True, True, True, True))
    df1 = df1.reset_index()

    # 2001 date
    df1['reference_date'] = pd.date_range('2001-01-01 00:30', periods=17520, freq='0.5H')
    # Weekdays
    df1['weekday'] = pd.DatetimeIndex(df1['offset_date']).strftime('%w')
    df1 = df1.astype({"weekday": int, })
    df1['weekday1'] = pd.DatetimeIndex(df1['offset_date']).day_name()

    return df1


def holiday_index_generator(df, input_data_dict):
    """
    This function generates the holiday index in the main dataframe. For the holiday period,
    the index is 0 and rest is 1.
    It takes lists of holiday period dictionary as input.
    """
    holiday_lists = input_data_dict['holiday_lists']    
    df['holiday_index'] = 1
    
    if holiday_lists is not None:
        for holiday_list in holiday_lists:
            start_day = holiday_list['start_day']
            start_month = holiday_list['start_month']
            end_day = holiday_list['end_day']
            end_month = holiday_list['end_month']            
            start_date = dt.datetime(2001, start_month, start_day)            
            end_date = dt.datetime(2001, end_month, end_day) + dt.timedelta(days=1)
            df.loc[(df['reference_date'] > start_date) & (df['reference_date'] <= end_date),'holiday_index'] = 0


    # print(f"Holiday Period = {365 - df['holiday_index'].sum()/48} days")

    return df


def generate_lighting_interval_data(df, input_data_dict):
    # Returns the Dataframe containing interval data, lighting load reduction, effective lighting load reduction
    lighting_hour_details_list = input_data_dict['lighting_hour_details_list']
    lighting_inputs_list = input_data_dict['lighting_inputs_list']
    lighting_boolean = input_data_dict['lighting_boolean']
    df.loc[:, 'lighting_load_reduction'] = 0    

    # Create new dataframe for lighting index

    lighting_index = pd.DataFrame(columns=None)
    lighting_index = df[['hours', 'weekday1']]
    # create index of all lighting inputs
    # lighting_hour_details = LightingHourDetail.objects.all().filter(scenario=scenario)
    power_reduction = 0
    if lighting_hour_details_list:
        for lighting_hour_detail in lighting_hour_details_list:
            x = lighting_hour_detail['lighting_type']
            lighting_index.loc[:,x] = 0
            # sum power reduction
            for lighting_input in lighting_inputs_list:
                if lighting_input['lighting_type_id'] == lighting_hour_detail['id']:                        
                    power_reduction = power_reduction + float(lighting_input['power_reduction'])

            for i in range(7):
                day = weekday_string(i)
                str1 = day.lower() + "_lighting_hour_1_start"
                # start_time = getattr(lighting_hour_detail, str1)
                start_time = lighting_hour_detail[str1]
                # startTime = lighting_hour_detail.monday_lighting_hour_1_start
                str2 = day.lower() + "_lighting_hour_1_end"
                end_time = lighting_hour_detail[str2]
                # print(start_time)
                # print(end_time)
                if (start_time != "N/A") and (end_time != "N/A"):
                    if (start_time == "All Times"):
                        lighting_index.loc[(lighting_index['weekday1'] == day), x] = 1
                    else:
                        lighting_index.loc[(lighting_index['weekday1'] == day) & (lighting_index['hours'] > int(start_time)) & (lighting_index['hours'] <= int(end_time)), x] = 1

                str1 = day.lower() + "_lighting_hour_2_start"
                start_time = lighting_hour_detail[str1]
                # startTime = lighting_hour_detail.monday_lighting_hour_1_start
                str2 = day.lower() + "_lighting_hour_2_end"
                end_time = lighting_hour_detail[str2]
                if (start_time != "N/A") and (end_time != "N/A"):
                    if (start_time == "All Times"):
                        lighting_index.loc[(lighting_index['weekday1'] == day), x] = 1
                    else:
                        lighting_index.loc[(lighting_index['weekday1'] == day) & (lighting_index['hours'] > int(start_time)) & (lighting_index['hours'] <= int(end_time)), x] = 1

            df.loc[:, 'lighting_load_reduction'] = df['lighting_load_reduction'] + \
                lighting_index[x]*power_reduction*df['holiday_index']*lighting_boolean
        # print(f"Total Lighting load reduction = {df['lighting_load_reduction'].sum()/2} kWh")

    return df


def add_solar_data(df, input_data_dict):

    solar_df = pd.DataFrame(input_data_dict['solar_data_datetime'], columns=['Datetime'])
    solar_df['kW'] = input_data_dict['solar_data_kW']

    # solar size
    solar_size = float(input_data_dict['simulation_parameter']['solar_size'])

    # Interpolate Solar kW
    solar_df['real_date'] = pd.TimedeltaIndex(
        solar_df['Datetime'], unit='d') + dt.datetime(1899, 12, 30)
    # rounding to nearest hour
    solar_df['rounded_date'] = solar_df['real_date'].dt.round('60min')
    
    
    solar_df_2 = pd.DataFrame()
    solar_df_2['rounded_date'] = pd.date_range(start='1/1/2001 00:30', end='1/1/2002 00:00', freq='0.5H')   
    solar_df_2['month'] = pd.DatetimeIndex(solar_df_2['rounded_date']).month
    solar_df_2 = pd.merge(solar_df_2,solar_df,how='outer',on='rounded_date')
    solar_df_2['original_solar'] = solar_df_2['kW']
    solar_df_2['kW'] = solar_df_2['kW'].interpolate()    
    # print(f"Sum kWh : {solar_df_2['kW'][solar_df_2['kW']>0].sum()/2} vs {solar_df['kW'].sum()}")
    solar_df_2['kW'].fillna(0,inplace=True) 

    solar_poe = 95
    solar_perc = []
    solar_perc_monthly = np.zeros((12,48))
    months = solar_df_2['month'].to_numpy().reshape(365,48)
    months = months[:,1]
    solar_kW = solar_df_2['kW'].to_numpy().reshape(365,48)
    total_length = 0
    for i in range(1,13):
        temp_solar_kW = solar_kW[months==i,:]
        len_month = temp_solar_kW.shape[0]
        temp_solar_perc = np.percentile(temp_solar_kW, 100-solar_poe ,axis = 0)
        solar_perc_monthly[i-1,:] = temp_solar_perc
        solar_perc = np.concatenate((solar_perc, np.tile(temp_solar_perc,len_month)))
        total_length = total_length + len_month*48

    df['solar_kW'] = solar_df_2['kW']*solar_size/100
    df['solar_kW_POE'] = solar_perc*solar_size/100

    return df


def calculate_load_after_system(df, input_data_dict):
    pfc_kvar = float(input_data_dict['simulation_parameter']['pfc_size'])
    target_pf = float(input_data_dict['simulation_parameter']['target_pf'])
    
    df['kvar'] = (df['kVA']**2 - df['kW']**2)**(1/2)

    # if toggler:
    #     # load after lighting kW and kVA
    #     df['load_after_lighting_kW'] = df.apply(lambda x: max(0, x['kW']-x['lighting_load_reduction']), axis=1)
    #     df['load_after_lighting_kVA'] = df.apply(lambda x: math.sqrt(x['load_after_lighting_kW']**2+x['kvar']**2), axis=1)
    #     df['load_after_solar_kW'] = df.apply(lambda x: max(0, x['load_after_lighting_kW']-x['solar_kW']), axis=1)
    #     df['spill'] = df.apply(lambda x: min(
    #     0, x['load_after_lighting_kW']-x['solar_kW']), axis=1)
    #     df['solar_utilised'] = df.apply(lambda x: min(
    #         x['load_after_lighting_kW'], x['solar_kW']), axis=1)

    #     simulation_parameter = SimulationParameter.objects.all().filter(scenario=scenario).first()
    #     pfc_kvar = float(simulation_parameter.pfc_size)
    #     df['new_kvars'] = df.apply(lambda x: max(0, x['kvar']-pfc_kvar), axis=1)

    #     df['new_kVA'] = df.apply(lambda x: math.sqrt(x['load_after_solar_kW']**2+x['new_kvars']**2), axis=1)

    #     kW_threshold = df['load_after_solar_kW'].max()/2
    #     target_pf = float(simulation_parameter.target_pf)    
    #     try:
    #         df['pfc_suggestion'] = df.apply(lambda x: max(0, x['kvar'] - math.sqrt((x['load_after_solar_kW']/(
    #             target_pf/100))**2 - x['load_after_solar_kW']**2)) if x.load_after_solar_kW > kW_threshold else 0, axis=1)
    #     except Exception as e:
    #         print(str(e))
        
    #     df['kW_after_solar_POE'] =  df.apply(lambda x: max(0, x['load_after_lighting_kW']-x['solar_kW_POE']), axis=1)
    #     df['kVA_after_solar_POE'] = df.apply(lambda x: math.sqrt(x['kW_after_solar_POE']**2+x['new_kvars']**2), axis=1)
    
    df['load_after_lighting_kW'] = np.maximum(0, df['kW']-df['lighting_load_reduction'])
    df['load_after_lighting_kVA'] = np.sqrt(df['load_after_lighting_kW']**2+df['kvar']**2)  
    df['load_after_solar_kW'] =  np.maximum(0, df['load_after_lighting_kW']-df['solar_kW'])
    df['spill'] = np.minimum(0, df['load_after_lighting_kW']-df['solar_kW'])
    df['solar_utilised'] = np.minimum(df['load_after_lighting_kW'], df['solar_kW'])
    
    
    df['new_kvars'] = np.maximum(0, df['kvar']-pfc_kvar)
    df['new_kVA'] = np.sqrt(df['load_after_solar_kW']**2+df['new_kvars']**2)
    kW_threshold = df['load_after_solar_kW'].max()/2    

    df['pfc_suggestion'] = np.maximum(0, df['kvar'] - np.sqrt((df['load_after_solar_kW']/(target_pf/100))**2 - df['load_after_solar_kW']**2)) 
    df.loc[df['load_after_solar_kW'] <= kW_threshold,'pfc_suggestion'] = 0
    
    df['kW_after_solar_POE'] =  np.maximum(0, df['load_after_lighting_kW']-df['solar_kW_POE'])
    df['kVA_after_solar_POE'] = np.sqrt(df['kW_after_solar_POE']**2+df['new_kvars']**2)

    return df


def calculate_power_bill(df, input_data_dict):
    energy_charges_list = input_data_dict['energy_charges_list']
    demand_charges_list = input_data_dict['demand_charges_list']
    fixed_charges_list = input_data_dict['fixed_charges_list']

    # Initialize Main Dataframe
    df_monthly_bill_summary = pd.DataFrame()
    df_monthly_tariff_summary = pd.DataFrame()
    df_monthly_bill_summary['months'] = np.arange(1,13)          
    df['peak_index'] = 0
    df_monthly_bill_summary['original_volume_charges'] = 0
    df_monthly_bill_summary['original_demand_charges'] = 0    
    df_monthly_bill_summary['after_lighting_volume_charges'] = 0
    df_monthly_bill_summary['after_lighting_demand_charges'] = 0    
    df_monthly_bill_summary['after_slp_volume_charges'] = 0
    df_monthly_bill_summary['after_slp_demand_charges'] = 0
    df_monthly_bill_summary['fixed_charges'] = 0
    
     
    # Energy Charges
    
    # Iteration through each energy charge
    for energy_charge in energy_charges_list:
        if energy_charge['include'] == "No":
            continue        
        tariff_name = energy_charge['tariff_name']
        tariff_type = energy_charge['tariff_type']
        amount = float(energy_charge['amount'])
        weekday_start_time = energy_charge['weekday_start_time']        
        weekday_end_time = energy_charge['weekday_end_time']
        weekend_start_time = energy_charge['weekend_start_time']
        weekend_end_time = energy_charge['weekend_end_time']
        months = energy_charge['months']
        category = energy_charge['category']
        # print(f'Months: {months}, {type(months)}')
        months = months.replace("{","")
        months = months.replace("}","")
        months = months.split(",")
        months = [int(i) for i in months]  # List Comprehension
        # print(f'Months: {months}, {type(months)}')
        # print(df.columns)
        # print(df.dtypes)

        if tariff_type == "Flat":
            load1 = np.zeros((12,))
            charges1 = np.zeros((12,))
            load2 = np.zeros((12,))
            charges2 = np.zeros((12,))
            load3 = np.zeros((12,))
            charges3 = np.zeros((12,))
            x1 = "original_vol_" + tariff_name + "_load"
            y1 = "original_vol_" + tariff_name + "_charges"
            x2 = "after_lighting_vol_" + tariff_name + "_load"
            y2 = "after_lighting_vol_" + tariff_name + "_charges"
            x3 = "after_slp_vol_" + tariff_name + "_load"
            y3 = "after_slp_vol_" + tariff_name + "_charges"
            # sub_df[x] = np.zeros((12,))
            # sub_df[y] = np.zeros((12,))
            for i in range(12):
                current_month = i+1
                load1[i] = df['kW'][df['month']==current_month].sum()/2
                load2[i] = df['load_after_lighting_kW'][df['month']==current_month].sum()/2
                load3[i] = df['load_after_solar_kW'][df['month']==current_month].sum()/2
                if current_month in months:             
                    charges1[i] = load1[i].sum()*amount
                    charges2[i] = load2[i].sum()*amount
                    charges3[i] = load3[i].sum()*amount
                else:
                    charges[i] = 0
            df_monthly_tariff_summary[x1] = load1
            df_monthly_tariff_summary[y1] = charges1
            df_monthly_tariff_summary[x2] = load2
            df_monthly_tariff_summary[y2] = charges2
            df_monthly_tariff_summary[x3] = load3
            df_monthly_tariff_summary[y3] = charges3
            df_monthly_bill_summary['original_volume_charges'] = df_monthly_bill_summary['original_volume_charges'] + charges1
            df_monthly_bill_summary['after_lighting_volume_charges'] = df_monthly_bill_summary['after_lighting_volume_charges'] + charges2
            df_monthly_bill_summary['after_slp_volume_charges'] = df_monthly_bill_summary['after_slp_volume_charges'] + charges3
        
        if tariff_type == "Peak":
            load1 = np.zeros((12,))
            charges1 = np.zeros((12,))
            load2 = np.zeros((12,))
            charges2 = np.zeros((12,))
            load3 = np.zeros((12,))
            charges3 = np.zeros((12,))
            x1 = "original_vol_" + tariff_name + "_load"
            y1 = "original_vol_" + tariff_name + "_charges"
            x2 = "after_lighting_vol_" + tariff_name + "_load"
            y2 = "after_lighting_vol_" + tariff_name + "_charges"
            x3 = "after_slp_vol_" + tariff_name + "_load"
            y3 = "after_slp_vol_" + tariff_name + "_charges"               
            for i in range(12):
                current_month = i+1
                #  weekday load
                if weekday_start_time == "All Times":                    
                    df.loc[(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6), 'peak_index'] = 1
                    load1[i] = df['kW'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) ].sum()/2
                    load2[i] = df['load_after_lighting_kW'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) ].sum()/2
                    load3[i] = df['load_after_solar_kW'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) ].sum()/2
                    
                elif weekday_start_time == "N/A":
                    load1[i] = 0
                    load2[i] = 0   
                    load3[i] = 0                    
                else:
                    weekday_start_time = float(weekday_start_time)
                    weekday_end_time = float(weekday_end_time)
                    df.loc[(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['hours']>weekday_start_time) & (df['hours']<=weekday_end_time), 'peak_index'] = 1
                    load1[i] = df['kW'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['hours']>weekday_start_time) & (df['hours']<=weekday_end_time) ].sum()/2
                    load2[i] = df['load_after_lighting_kW'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['hours']>weekday_start_time) & (df['hours']<=weekday_end_time) ].sum()/2
                    load3[i] = df['load_after_solar_kW'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['hours']>weekday_start_time) & (df['hours']<=weekday_end_time) ].sum()/2
                    
                # weekend load
                if weekend_start_time == "All Times":                    
                    df.loc[(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)), 'peak_index'] = 1
                    load1[i] = load1[i] + df['kW'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6))].sum()/2
                    load2[i] = load2[i] + df['load_after_lighting_kW'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6))].sum()/2
                    load3[i] = load3[i] + df['load_after_solar_kW'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6))].sum()/2
                    
                elif weekend_start_time != "N/A":                    
                    weekend_start_time = float(weekend_start_time)
                    weekend_end_time = float(weekend_end_time)
                    df.loc[(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['hours']>weekend_start_time) & (df['hours']<=weekend_end_time), 'peak_index' ] = 1 
                    load1[i] = load1[i] + df['kW'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['hours']>weekend_start_time) & (df['hours']<=weekend_end_time) ].sum()/2
                    load2[i] = load2[i] + df['load_after_lighting_kW'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['hours']>weekend_start_time) & (df['hours']<=weekend_end_time) ].sum()/2
                    load3[i] = load3[i] + df['load_after_solar_kW'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['hours']>weekend_start_time) & (df['hours']<=weekend_end_time) ].sum()/2
                                
                if current_month in months:             
                    charges1[i] = load1[i]*amount
                    charges2[i] = load2[i]*amount
                    charges3[i] = load3[i]*amount
                else:
                    charges1[i] = 0
                    charges2[i] = 0
                    charges3[i] = 0
            
            df_monthly_tariff_summary[x1] = load1
            df_monthly_tariff_summary[y1] = charges1
            df_monthly_tariff_summary[x2] = load2
            df_monthly_tariff_summary[y2] = charges2
            df_monthly_tariff_summary[x3] = load3
            df_monthly_tariff_summary[y3] = charges3
            df_monthly_bill_summary['original_volume_charges'] = df_monthly_bill_summary['original_volume_charges'] + charges1
            df_monthly_bill_summary['after_lighting_volume_charges'] = df_monthly_bill_summary['after_lighting_volume_charges'] + charges2
            df_monthly_bill_summary['after_slp_volume_charges'] = df_monthly_bill_summary['after_slp_volume_charges'] + charges3
        
    # Iteration through each energy charge   
    for energy_charge in energy_charges_list:
        if energy_charge['include'] == "No":
            continue        
        tariff_name = energy_charge['tariff_name']
        tariff_type = energy_charge['tariff_type']
        amount = float(energy_charge['amount'])            
        months = energy_charge['months']
        category = energy_charge['category']            
        months = months.replace("{","")
        months = months.replace("}","")
        months = months.split(",")
        months = [int(i) for i in months]  # List Comprehension
        
        if tariff_type == "Offpeak":
            load1 = np.zeros((12,))
            charges1 = np.zeros((12,))
            load2 = np.zeros((12,))
            charges2 = np.zeros((12,))
            load3 = np.zeros((12,))
            charges3 = np.zeros((12,))
            x1 = "original_vol_" + tariff_name + "_load"
            y1 = "original_vol_" + tariff_name + "_charges"
            x2 = "after_lighting_vol_" + tariff_name + "_load"
            y2 = "after_lighting_vol_" + tariff_name + "_charges"
            x3 = "after_slp_vol_" + tariff_name + "_load"
            y3 = "after_slp_vol_" + tariff_name + "_charges"
            for i in range(12):
                current_month = i+1
                load1[i] = df['kW'][(df['month']==current_month) & (df['peak_index']==0)].sum()/2
                load2[i] = df['load_after_lighting_kW'][(df['month']==current_month) & (df['peak_index']==0)].sum()/2
                load3[i] = df['load_after_solar_kW'][(df['month']==current_month) & (df['peak_index']==0)].sum()/2
                if current_month in months:             
                    charges1[i] = load1[i].sum()*amount
                    charges2[i] = load2[i].sum()*amount
                    charges3[i] = load3[i].sum()*amount
                else:
                    charges1[i] = 0
                    charges2[i] = 0
                    charges3[i] = 0

            df_monthly_tariff_summary[x1] = load1
            df_monthly_tariff_summary[y1] = charges1
            df_monthly_tariff_summary[x2] = load2
            df_monthly_tariff_summary[y2] = charges2
            df_monthly_tariff_summary[x3] = load3
            df_monthly_tariff_summary[y3] = charges3
            df_monthly_bill_summary['original_volume_charges'] = df_monthly_bill_summary['original_volume_charges'] + charges1
            df_monthly_bill_summary['after_lighting_volume_charges'] = df_monthly_bill_summary['after_lighting_volume_charges'] + charges2
            df_monthly_bill_summary['after_slp_volume_charges'] = df_monthly_bill_summary['after_slp_volume_charges'] + charges3
    

    # Demand Charges

    # Iteration through each demand charge
    for demand_charge in demand_charges_list:
        if demand_charge['include'] == "No":
            continue        
        tariff_name = demand_charge['tariff_name']
        tariff_type = demand_charge['tariff_type']
        chargeable_power = float(demand_charge['chargeable_power'])
        amount = float(demand_charge['amount'])
        weekday_start_time = demand_charge['weekday_start_time']        
        weekday_end_time = demand_charge['weekday_end_time']
        weekend_start_time = demand_charge['weekend_start_time']
        weekend_end_time = demand_charge['weekend_end_time']
        chargeable_power_type = demand_charge['chargeable_power_type']
        months = demand_charge['months']
        threshold = demand_charge['threshold']
        category = demand_charge['category']
        
        # Converting months to integer values 
        months = months.replace("{","")
        months = months.replace("}","")
        months = months.split(",")
        months = [int(i) for i in months]  # List Comprehension
        # Converting threshold to integer values 
        threshold = threshold.replace("{","")
        threshold = threshold.replace("}","")
        threshold = threshold.split(",")
        threshold = [int(i) for i in threshold]  # List Comprehension
        threshold_start = threshold[0]
        threshold_end = threshold[1]

        if tariff_type == "Monthly Peak":
            weekday_load1 = np.zeros((12,))
            weekend_load1 = np.zeros((12,))
            weekday_load2 = np.zeros((12,))
            weekend_load2 = np.zeros((12,))
            weekday_load3 = np.zeros((12,))
            weekend_load3 = np.zeros((12,))
            load1 = np.zeros((12,))
            charges1 = np.zeros((12,))
            load2 = np.zeros((12,))
            charges2 = np.zeros((12,))
            load3 = np.zeros((12,))
            charges3 = np.zeros((12,))
            x1 = "original_dem_" + tariff_name + "_load"
            y1 = "original_dem_" + tariff_name + "_charges"
            x2 = "after_lighting_dem_" + tariff_name + "_load"
            y2 = "after_lighting_dem_" + tariff_name + "_charges"
            x3 = "after_slp_dem_" + tariff_name + "_load"
            y3 = "after_slp_dem_" + tariff_name + "_charges"
            if x1 in df_monthly_tariff_summary.columns:
                dup_flag = 1
            else:
                dup_flag = 0
            
            if chargeable_power_type == "kW":
                df['original_temp_load'] = df['kW']
                df['after_lighting_temp_load'] = df['load_after_lighting_kW']
                df['after_slp_temp_load'] = df['kW_after_solar_POE']
            else:                
                df['original_temp_load'] = df['kVA']
                df['after_lighting_temp_load'] = df['load_after_lighting_kVA']
                df['after_slp_temp_load'] = df['kVA_after_solar_POE']

            for i in range(12):
                current_month = i+1
                #  weekday load
                if weekday_start_time == "All Times":
                    weekday_load1[i] = df['original_temp_load'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['original_temp_load']>threshold_start) & (df['original_temp_load']<=threshold_end) ].max()
                    weekday_load2[i] = df['after_lighting_temp_load'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['after_lighting_temp_load']>threshold_start) & (df['after_lighting_temp_load']<=threshold_end) ].max()
                    weekday_load3[i] = df['after_slp_temp_load'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['after_slp_temp_load']>threshold_start) & (df['after_slp_temp_load']<=threshold_end) ].max()               
                elif weekday_start_time == "N/A":
                    weekday_load1[i] = 0
                    weekday_load2[i] = 0                    
                    weekday_load3[i] = 0
                else:
                    weekday_start_time = float(weekday_start_time)
                    weekday_end_time = float(weekday_end_time)
                    weekday_load1[i] = df['original_temp_load'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['hours']>weekday_start_time) & (df['hours']<=weekday_end_time) & (df['original_temp_load']>threshold_start) & (df['original_temp_load']<=threshold_end) ].max()
                    weekday_load2[i] = df['after_lighting_temp_load'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['hours']>weekday_start_time) & (df['hours']<=weekday_end_time) & (df['after_lighting_temp_load']>threshold_start) & (df['after_lighting_temp_load']<=threshold_end) ].max()
                    weekday_load3[i] = df['after_slp_temp_load'][(df['month']==current_month) & (df['weekday']>0) & (df['weekday']<6) & (df['hours']>weekday_start_time) & (df['hours']<=weekday_end_time) & (df['after_slp_temp_load']>threshold_start) & (df['after_slp_temp_load']<=threshold_end) ].max()
                # weekend load
                if weekend_start_time == "All Times":                    
                    weekend_load1[i] = df['original_temp_load'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['original_temp_load']>threshold_start) & (df['original_temp_load']<=threshold_end)].max() 
                    weekend_load2[i] = df['after_lighting_temp_load'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['after_lighting_temp_load']>threshold_start) & (df['after_lighting_temp_load']<=threshold_end)].max() 
                    weekend_load3[i] = df['after_slp_temp_load'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['after_slp_temp_load']>threshold_start) & (df['after_slp_temp_load']<=threshold_end)].max()                    
                elif weekend_start_time == "N/A":
                    weekend_load1[i] = 0
                    weekend_load2[i] = 0
                    weekend_load3[i] = 0
                else:
                    weekend_start_time = float(weekend_start_time)
                    weekend_end_time = float(weekend_end_time)
                    weekend_load1[i] = df['original_temp_load'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['hours']>weekend_start_time) & (df['hours']<=weekend_end_time) & (df['original_temp_load']>threshold_start) & (df['original_temp_load']<=threshold_end) ].max()
                    weekend_load2[i] = df['after_lighting_temp_load'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['hours']>weekend_start_time) & (df['hours']<=weekend_end_time) & (df['after_lighting_temp_load']>threshold_start) & (df['after_lighting_temp_load']<=threshold_end) ].max()
                    weekend_load3[i] = df['after_slp_temp_load'][(df['month']==current_month) & ((df['weekday']==0) | (df['weekday']==6)) & (df['hours']>weekend_start_time) & (df['hours']<=weekend_end_time) & (df['after_slp_temp_load']>threshold_start) & (df['after_slp_temp_load']<=threshold_end) ].max()                      
                
                if current_month in months: 
                    if dup_flag == 1:
                        load1[i] = max(df_monthly_tariff_summary[x1][i],weekday_load1[i],weekend_load1[i])
                        load2[i] = max(df_monthly_tariff_summary[x2][i],weekday_load2[i],weekend_load2[i])
                        load3[i] = max(df_monthly_tariff_summary[x3][i],weekday_load3[i],weekend_load3[i])     
                    else:
                        load1[i] = max(weekday_load1[i],weekend_load1[i])
                        load2[i] = max(weekday_load2[i],weekend_load2[i])
                        load3[i] = max(weekday_load3[i],weekend_load3[i])            
                    charges1[i] = load1[i]*amount
                    charges2[i] = load2[i]*amount
                    charges3[i] = load3[i]*amount
                else:
                    charges1[i] = 0
                    charges2[i] = 0
                    charges3[i] = 0
            
            
            if dup_flag == 1:
                df_monthly_bill_summary['original_demand_charges'] = df_monthly_bill_summary['original_demand_charges'] - df_monthly_tariff_summary[y1]
                df_monthly_bill_summary['after_lighting_demand_charges'] = df_monthly_bill_summary['after_lighting_demand_charges'] - df_monthly_tariff_summary[y2]
                df_monthly_bill_summary['after_slp_demand_charges'] = df_monthly_bill_summary['after_slp_demand_charges'] - df_monthly_tariff_summary[y3]
            df_monthly_tariff_summary[x1] = load1
            df_monthly_tariff_summary[y1] = charges1
            df_monthly_tariff_summary[x2] = load2
            df_monthly_tariff_summary[y2] = charges2
            df_monthly_tariff_summary[x3] = load3
            df_monthly_tariff_summary[y3] = charges3
            df_monthly_bill_summary['original_demand_charges'] = df_monthly_bill_summary['original_demand_charges'] + charges1
            df_monthly_bill_summary['after_lighting_demand_charges'] = df_monthly_bill_summary['after_lighting_demand_charges'] + charges2
            df_monthly_bill_summary['after_slp_demand_charges'] = df_monthly_bill_summary['after_slp_demand_charges'] + charges3
            

        if tariff_type == "Capacity":            
            load = np.zeros((12,))
            charges = np.zeros((12,))            
            x1 = "original_dem_" + tariff_name + "_load"
            y1 = "original_dem_" + tariff_name + "_charges"
            x2 = "after_lighting_dem_" + tariff_name + "_load"
            y2 = "after_lighting_dem_" + tariff_name + "_charges"
            x3 = "after_slp_dem_" + tariff_name + "_load"
            y3 = "after_slp_dem_" + tariff_name + "_charges"
            if x1 in df_monthly_tariff_summary.columns:
                dup_flag = 1
            else:
                dup_flag = 0               

            for i in range(12):
                current_month = i+1
                load[i] = chargeable_power
                if current_month in months:                                               
                    charges[i] = load[i]*amount
                else:
                    charges[i] = 0

            if dup_flag == 1:
                df_monthly_bill_summary['original_demand_charges'] = df_monthly_bill_summary['original_demand_charges'] - df_monthly_tariff_summary[y1]
                df_monthly_bill_summary['after_lighting_demand_charges'] = df_monthly_bill_summary['after_lighting_demand_charges'] - df_monthly_tariff_summary[y2]
                df_monthly_bill_summary['after_slp_demand_charges'] = df_monthly_bill_summary['after_slp_demand_charges'] - df_monthly_tariff_summary[y3]
            df_monthly_tariff_summary[x1] = load
            df_monthly_tariff_summary[y1] = charges
            df_monthly_tariff_summary[x2] = load
            df_monthly_tariff_summary[y2] = charges
            df_monthly_tariff_summary[x3] = load
            df_monthly_tariff_summary[y3] = charges
            df_monthly_bill_summary['original_demand_charges'] = df_monthly_bill_summary['original_demand_charges'] + charges
            df_monthly_bill_summary['after_lighting_demand_charges'] = df_monthly_bill_summary['after_lighting_demand_charges'] + charges
            df_monthly_bill_summary['after_slp_demand_charges'] = df_monthly_bill_summary['after_slp_demand_charges'] + charges
            

       
    # Fixed Charges
    
    # Iteration through each fixed charge
    for fixed_charge in fixed_charges_list:
        if fixed_charge['include'] == "No":
            continue        
        tariff_name = fixed_charge['tariff_name']        
        amount = float(fixed_charge['amount'])
        frequency = fixed_charge['frequency']    
        category = fixed_charge['category']        
                    
        freq_per_month = np.zeros((12,))
        charges = np.zeros((12,))
        x = "fix_" + tariff_name + "_frequency"
        y = "fix_" + tariff_name + "_charges" 
        
        
        for i in range(12):
            current_month = i+1
            if frequency == "Monthly":
                freq_per_month[i] = 1
            else:
                freq_per_month[i] = df['month'][df['month'] == current_month].count()/48
            
            charges[i] = freq_per_month[i]*amount

        df_monthly_tariff_summary[x] = freq_per_month
        df_monthly_tariff_summary[y] = charges
        df_monthly_bill_summary['fixed_charges'] = df_monthly_bill_summary['fixed_charges'] + charges 

    df_monthly_bill_summary['lighting_bill_savings'] = df_monthly_bill_summary['original_volume_charges'] + df_monthly_bill_summary['original_demand_charges'] - df_monthly_bill_summary['after_lighting_volume_charges'] - df_monthly_bill_summary['after_lighting_demand_charges']
    df_monthly_bill_summary['solarpfc_bill_savings'] = df_monthly_bill_summary['after_lighting_volume_charges'] + df_monthly_bill_summary['after_lighting_demand_charges']- df_monthly_bill_summary['after_slp_volume_charges'] - df_monthly_bill_summary['after_slp_demand_charges']
    df_monthly_bill_summary['lighting_energy_savings_proportion'] = (df_monthly_bill_summary['original_volume_charges'] - df_monthly_bill_summary['after_lighting_volume_charges']) / df_monthly_bill_summary['lighting_bill_savings']
    df_monthly_bill_summary['solarpfc_energy_savings_proportion'] = (df_monthly_bill_summary['after_lighting_volume_charges'] - df_monthly_bill_summary['after_slp_volume_charges']) / df_monthly_bill_summary['solarpfc_bill_savings']

    df_monthly_bill_summary.fillna(0, inplace=True)
    # print('-------------------Monthly Bill Summary-----------------------')
    # print(df_monthly_bill_summary)
    
    
    return df, df_monthly_bill_summary, df_monthly_tariff_summary


def calculate_load_summary(df):
    # Monthly Site Load (kWhs, peakkW, peakkVA, PF)
    # Monthly Site Load after Lighting (kWhs, peakkW, peakkVA, PF)
    # Monthly Site Load after Lighting, Solar and PFC (kWhs, peakkW, peakkVA, PF)
    
    # Initialize Main Dataframe
    df_monthly_load_summary = pd.DataFrame()
    df_monthly_load_summary['months'] = np.arange(1,13)
    
    df_temp_1 = df.groupby(['month']).sum().reset_index()
    df_temp_2 = df.groupby(['month']).max().reset_index()
    # print('----------------df temp 2- --------------------')
    # print(df_temp_2)
    df_monthly_load_summary['original_kwhs'] = df_temp_1['kW']/2
    df_monthly_load_summary['original_kw'] = df_temp_2['kW']
    df_monthly_load_summary['original_kva'] = df_temp_2['kVA']
    df_monthly_load_summary['after_lighting_kwhs'] = df_temp_1['load_after_lighting_kW']/2
    df_monthly_load_summary['after_lighting_kw'] = df_temp_2['load_after_lighting_kW']
    df_monthly_load_summary['after_lighting_kva'] = df_temp_2['load_after_lighting_kVA']
    df_monthly_load_summary['after_slp_kwhs'] = df_temp_1['load_after_solar_kW']/2
    df_monthly_load_summary['after_slp_kw'] = df_temp_2['kW_after_solar_POE']
    df_monthly_load_summary['after_slp_kva'] = df_temp_2['kVA_after_solar_POE']
    df_monthly_load_summary['solar_ideal'] = df_temp_1['solar_kW']/2
    df_monthly_load_summary['solar_actual'] = df_temp_1['solar_utilised']/2
    df_monthly_load_summary['solar_utilisation'] = df_monthly_load_summary['solar_actual'] / df_monthly_load_summary['solar_ideal'] 

    # print('----------------df temp 1 - --------------------')
    # print(df_temp_1[['kW','load_after_lighting_kW','solar_kW','load_after_solar_kW','solar_utilised']]/2)
    # print('----------------df Load Summary - --------------------')
    # print(df_monthly_load_summary)
    return df_monthly_load_summary


def calculate_cashflow(df, df_monthly_bill_summary, df_monthly_load_summary, input_data_dict):
    

    # cashflow_start_date = dt.datetime.strptime(input_data_dict['cashflow_start_date'], '%Y-%m-%d')
    tariff_escalations_list = input_data_dict['tariff_escalations_list']
    price_forecast_override_list = input_data_dict['price_forecast_override_list']
    escalations_override_list = input_data_dict['escalations_override_list']    
    lighting_inputs_list = input_data_dict['lighting_inputs_list']
    include_solar_export = input_data_dict['include_solar_export']
    lgc_flag = input_data_dict['lgc_flag']
    panel_degradation_per_year = input_data_dict['panel_degradation']
    certificate_prices_dict = input_data_dict['certificate_prices_dict']
    solar_export_dict = input_data_dict['solar_export_dict']

    df_monthly_cashflow = pd.DataFrame()

    # Save in Database
    start_month = input_data_dict['program_overrides_dict']['cashflow_start_month']
    start_year = input_data_dict['program_overrides_dict']['cashflow_start_year']
    start_date_string = '15/' + str(start_month) + '/' + str(start_year)
    # panel_degradation_per_year = 0.5/100

    # Timings (25 years)
    num_years = 25
    df_monthly_cashflow['date'] = pd.date_range(start=start_date_string, periods=num_years*12 , freq='M')
    df_monthly_cashflow['calendar_month'] = pd.DatetimeIndex(df_monthly_cashflow['date']).month
    df_monthly_cashflow['calendar_year'] = pd.DatetimeIndex(df_monthly_cashflow['date']).year
    df_monthly_cashflow['system_month'] = np.arange(start=1,stop=num_years*12+1,step=1)
    df_monthly_cashflow['system_year'] = np.ceil(np.arange(start=1,stop=num_years*12+1,step=1)/12)
    

    # ------------- Intermediate Calculations ------------------------------------------------------------

    # Panel Degradation

    df_monthly_cashflow['panel_performance'] = 1 - panel_degradation_per_year*(df_monthly_cashflow['system_year']-1)

    panel_performance = np.ones((num_years*12))
    system_year = df_monthly_cashflow['system_year'].to_numpy()

    for i in range(len(panel_performance)):
        if i==0:
            panel_performance[i] = 1
        else:
            if system_year[i] == system_year[i-1]:
                panel_performance[i] = panel_performance[i-1]
            else:
                panel_performance[i] = panel_performance[i-1]*(1 - panel_degradation_per_year)
    
    df_monthly_cashflow['panel_performance'] = panel_performance
    

    # Escalations
    ### Normal Escalations
    start_year = 2019
    num_years_2 = 30
    
    escalations_table = pd.DataFrame()
    escalations_table_1 = np.zeros((num_years_2,4))

    
    for i in range(num_years_2):
        escalations_table_1[i,0] = start_year + i

    escalations_table['year'] = escalations_table_1[:,0]


    # escalations_table_1[0,1] = float(getattr(TariffEscalations.objects.filter(year=2019).first(), state.lower()))
    # escalations_table_1[1,1] = getattr(TariffEscalations.objects.filter(year=2020).first(), state.lower())
    # escalations_table_1[2,1] = getattr(TariffEscalations.objects.filter(year=2021).first(), state.lower())
    # escalations_table_1[3,1] = getattr(TariffEscalations.objects.filter(year=2022).first(), state.lower())
    # escalations_table_1[4,1] = getattr(TariffEscalations.objects.filter(year=2023).first(), state.lower())
    # escalations_table_1[5,1] = getattr(TariffEscalations.objects.filter(year=2024).first(), state.lower())
    # escalations_table_1[6,1] = getattr(TariffEscalations.objects.filter(year=2025).first(), state.lower())
    # escalations_table_1[7,1] = getattr(TariffEscalations.objects.filter(year=2026).first(), state.lower())
    # escalations_table_1[8,1] = getattr(TariffEscalations.objects.filter(year=2027).first(), state.lower())
    for i in range(num_years_2):
        if i > 8:
            escalations_table_1[i,1] = escalations_table_1[8,1]
        else:
            escalations_table_1[i,1] = tariff_escalations_list[i]

    
    
    escalations_table['escalations'] = escalations_table_1[:,1]

    counter = 0
    for forecast in price_forecast_override_list:
        if forecast is None:
            escalations_table_1[counter,2] = escalations_table_1[counter,1]
        else:
            escalations_table_1[counter,2] = forecast
        counter = counter + 1


    # if not price_forecast_override:
    #     escalations_table_1[0,2] = escalations_table_1[0,1]
    #     escalations_table_1[1,2] = escalations_table_1[1,1]
    #     escalations_table_1[2,2] = escalations_table_1[2,1]
    #     escalations_table_1[3,2] = escalations_table_1[3,1]
    #     escalations_table_1[4,2] = escalations_table_1[4,1]
    #     escalations_table_1[5,2] = escalations_table_1[5,1]
    #     escalations_table_1[6,2] = escalations_table_1[6,1]
    #     escalations_table_1[7,2] = escalations_table_1[7,1]
    #     escalations_table_1[8,2] = escalations_table_1[8,1]
    # else:
    #     escalations_table_1[0,2] = price_forecast_override.year_2019
    #     escalations_table_1[1,2] = price_forecast_override.year_2020
    #     escalations_table_1[2,2] = price_forecast_override.year_2021
    #     escalations_table_1[3,2] = price_forecast_override.year_2022
    #     escalations_table_1[4,2] = price_forecast_override.year_2023
    #     escalations_table_1[5,2] = price_forecast_override.year_2024
    #     escalations_table_1[6,2] = price_forecast_override.year_2025
    #     escalations_table_1[7,2] = price_forecast_override.year_2026
    #     escalations_table_1[8,2] = price_forecast_override.year_2027

    for i in range(num_years_2):
        if i > 8:
            escalations_table_1[i,2] = escalations_table_1[8,2]

    escalations_table['price_forecast'] = escalations_table_1[:,2]

    for i in range(num_years_2):
        if np.isnan(escalations_table_1[i,2]):
            escalations_table_1[i,3] = escalations_table_1[i,1]
        else:
            escalations_table_1[i,3] = escalations_table_1[i,2]

    escalations_table['price_forecast_override'] = escalations_table_1[:,3]
    
    df_monthly_cashflow['escalations'] = 0
    
    
    for i in range(num_years_2):
        df_monthly_cashflow.loc[(df_monthly_cashflow['calendar_month'] == 1) & (df_monthly_cashflow['calendar_year'] == int(escalations_table_1[i,0])), 'escalations'] = escalations_table_1[i,3]
    
    
    for escalations_override in escalations_override_list:
        month_temp = escalations_override['month_temp']
        year_temp = escalations_override['year_temp']
        override_temp = escalations_override['override_temp']
        if month_temp and year_temp and override_temp:
            df_monthly_cashflow.loc[(df_monthly_cashflow['calendar_month'] == month_temp) & (df_monthly_cashflow['calendar_year'] == year_temp), 'escalations'] = override_temp

    escalations = df_monthly_cashflow['escalations'].to_numpy()
    escalations_multiplier = np.zeros((len(escalations)))
    for i in range(len(escalations)):
        if i ==0:
            escalations_multiplier[i] = 1*(1+float(escalations[i])/100)
        else:
            escalations_multiplier[i] = escalations_multiplier[i-1]*(1+float(escalations[i])/100)

    df_monthly_cashflow['escalations_multiplier'] = escalations_multiplier

    
    # LGC Prices
    df_monthly_cashflow['LGC_price'] = 0.0        
    
    for year_temp in range(2019,2031):
        key_temp = "LGCprice" + str(year_temp)
        lgc_price_temp = float(certificate_prices_dict[key_temp])
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_year'] == year_temp, 'LGC_price'] = lgc_price_temp
    

    # Feed in rates

    df_monthly_cashflow['Feed_in_rates'] = 0.0    
        
    if include_solar_export == 1:
        for i in range(30):
            year_temp = i+2019
            key_temp =  "year_" + str(year_temp)
            if year_temp < 2032:
                feedin_price_temp = solar_export_dict[key_temp]
            else:
                feedin_price_temp = solar_export_dict['year_2031']

            if feedin_price_temp is None:
                feedin_price_temp = 0
            else:
                feedin_price_temp = float(feedin_price_temp)

            df_monthly_cashflow.loc[df_monthly_cashflow['calendar_year'] == year_temp, 'Feed_in_rates'] = feedin_price_temp
    


    
    # Lighting, Solar and PFC Energy Savings Proportion
    df_monthly_cashflow['lighting_energy_savings_proportion'] = 0.0
    df_monthly_cashflow['solarpfc_energy_savings_proportion'] = 0.0

    for i in range(12):
        month_temp = i + 1 
        lighting_energy_proportion = df_monthly_bill_summary['lighting_energy_savings_proportion'][i]
        solarpfc_energy_proportion = df_monthly_bill_summary['solarpfc_energy_savings_proportion'][i]        
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'lighting_energy_savings_proportion'] = lighting_energy_proportion
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'solarpfc_energy_savings_proportion'] = solarpfc_energy_proportion

    


    # ---------------------------Lighting Degradation------------------------------------------------
    # for each lighting input, calculate the monthly degradation factors
    mu = 75000
    sigma = 25000/3
    stds = np.arange(-3,3.5,0.5)
    normlist = np.zeros(13,)
    lighting_hours = np.zeros(13,)
    counter = 0
    for i in stds:
        normlist[counter] = normaldist(mu,sigma,i)
        lighting_hours[counter] = i*sigma + mu
        counter = counter + 1
    
    df_lighting_degradation = pd.DataFrame(data=normlist, columns=['probabilities'])
    df_lighting_degradation['lighting_hours'] = lighting_hours
    df_lighting_degradation['perc'] = df_lighting_degradation['probabilities']/df_lighting_degradation['probabilities'].sum()
    df_lighting_degradation['cumulative_perc'] = df_lighting_degradation['perc'].cumsum()
    df_lighting_degradation_cashflow = df_monthly_cashflow[['system_month']]
    df_lighting_degradation_cashflow.loc[:, 'total_maintenance_savings'] = 0
    df_lighting_degradation_cashflow.loc[:, 'total_cummulative_loss'] = 0

    counter = 0
    start_maintenance_savings = 0.0
    if lighting_inputs_list:
        for lighting_input in lighting_inputs_list:
            hours_per_month = 50000 / lighting_input['led_life_in_months']
            maintenance_savings = float(lighting_input['maintenance_savings']) / 12
            start_maintenance_savings = start_maintenance_savings + maintenance_savings
            counter = counter + 1
            start_month = 'start_month_' + str(counter)
            end_month = 'end_month_' + str(counter) 
            mnt_savings = 'maintenance_savings' + str(counter)  
            cum_loss = 'cummulative_loss' + str(counter)  
            rng = df_lighting_degradation.shape[0]        
            df_lighting_degradation[start_month] = np.around(df_lighting_degradation['lighting_hours']/hours_per_month)
            df_lighting_degradation[end_month] = df_lighting_degradation[start_month].shift(-1)
            df_lighting_degradation[end_month][rng-1] = max(301,df_lighting_degradation[start_month][rng-1])            
            df_lighting_degradation_cashflow.loc[:, cum_loss] = 0.0            
            for i in range(rng):
                start_month_temp = df_lighting_degradation[start_month][i]
                end_month_temp = df_lighting_degradation[end_month][i]
                temp_cum_perc = df_lighting_degradation['cumulative_perc'][i]
                df_lighting_degradation_cashflow.loc[ (df_lighting_degradation_cashflow['system_month'] > start_month_temp) & (df_lighting_degradation_cashflow['system_month'] <= end_month_temp) ,cum_loss] = temp_cum_perc
            df_lighting_degradation_cashflow.loc[:, mnt_savings] = (1-df_lighting_degradation_cashflow[cum_loss])*maintenance_savings
            df_lighting_degradation_cashflow.loc[:, 'total_maintenance_savings'] = df_lighting_degradation_cashflow['total_maintenance_savings']  + df_lighting_degradation_cashflow[mnt_savings]
        
        df_lighting_degradation_cashflow.loc[:,'total_cummulative_loss'] = (start_maintenance_savings - df_lighting_degradation_cashflow['total_maintenance_savings'] ) / start_maintenance_savings

    df_monthly_cashflow['total_cummulative_loss'] = df_lighting_degradation_cashflow['total_cummulative_loss']
    

    #------------------------------------ Site Loads -------------------------------------------
    df_monthly_cashflow['site_load_before'] = 0.0
    df_monthly_cashflow['site_load_after_lighting'] = 0.0
    df_monthly_cashflow['site_load_after_slp'] = 0.0
    
    for i in range(12):
        month_temp = i +1 
        site_load_before = df_monthly_load_summary['original_kwhs'][i]
        site_load_after_lighting = df_monthly_load_summary['after_lighting_kwhs'][i]
        # site_load_after_slp = df_monthly_load_summary['after_slp_kwhs'][i]
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'site_load_before'] = site_load_before
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'site_load_after_lighting'] = site_load_after_lighting
        # df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'site_load_after_slp'] = site_load_after_slp

    df_monthly_cashflow['site_load_after_lighting'] = df_monthly_cashflow['site_load_before'] - (df_monthly_cashflow['site_load_before']-df_monthly_cashflow['site_load_after_lighting'])*(1-df_lighting_degradation_cashflow['total_cummulative_loss'])
    

    #-------------------------Lighting Load Reduction--------------------
    df_monthly_cashflow['lighting_load_reduction'] = df_monthly_cashflow['site_load_before'] - df_monthly_cashflow['site_load_after_lighting']

    #-------------------------Solar Generation--------------------------
    df_monthly_cashflow['solar_generation_ideal'] = 0.0
    df_monthly_cashflow['solar_generation_utilised'] = 0.0
    df_monthly_cashflow['solar_generation_spill'] = 0.0

    for i in range(12):
        month_temp = i + 1
        solar_generation_ideal = df_monthly_load_summary['solar_ideal'][i]
        solar_generation_utilised = df_monthly_load_summary['solar_actual'][i]
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'solar_generation_ideal'] = solar_generation_ideal
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'solar_generation_utilised'] = solar_generation_utilised

    df_monthly_cashflow['solar_generation_ideal'] = df_monthly_cashflow['solar_generation_ideal']*df_monthly_cashflow['panel_performance']
    df_monthly_cashflow['solar_generation_utilised'] = df_monthly_cashflow['solar_generation_utilised']*df_monthly_cashflow['panel_performance']
    if include_solar_export == 1:
        df_monthly_cashflow['solar_generation_spill'] = df_monthly_cashflow['solar_generation_ideal'] - df_monthly_cashflow['solar_generation_utilised']


    df_monthly_cashflow['site_load_after_slp']= df_monthly_cashflow['site_load_after_lighting'] - df_monthly_cashflow['solar_generation_utilised'] 

    

    #----------------------Electricity Bills----------------------------------
    df_monthly_cashflow['electricity_bill_original'] = 0.0
    df_monthly_cashflow['electricity_bill_after_lighting'] = 0.0
    df_monthly_cashflow['electricity_bill_after_slp'] = 0.0

    for i in range(12):
        month_temp = i + 1
        fixed_charges = df_monthly_bill_summary['fixed_charges'][i]
        volume_charges_original = df_monthly_bill_summary['original_volume_charges'][i]
        demand_charges_original = df_monthly_bill_summary['original_demand_charges'][i]
        volume_charges_after_lighting = df_monthly_bill_summary['after_lighting_volume_charges'][i]
        demand_charges_after_lighting = df_monthly_bill_summary['after_lighting_demand_charges'][i]
        volume_charges_after_slp = df_monthly_bill_summary['after_slp_volume_charges'][i]
        demand_charges_after_slp = df_monthly_bill_summary['after_slp_demand_charges'][i]
        temp_bill_original = volume_charges_original + demand_charges_original + fixed_charges
        temp_bill_after_lighting = volume_charges_after_lighting + demand_charges_after_lighting + fixed_charges
        temp_bill_after_slp = volume_charges_after_slp + demand_charges_after_slp + fixed_charges
        temp_solar_utilised = df_monthly_load_summary['solar_actual'][i]
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'electricity_bill_original'] = temp_bill_original
        df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'electricity_bill_after_lighting'] = temp_bill_after_lighting
        if df_monthly_cashflow['solar_generation_ideal'].sum() > 0:
            df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'electricity_bill_after_slp'] = (temp_bill_after_lighting - temp_bill_after_slp) / temp_solar_utilised
        else:
            df_monthly_cashflow.loc[df_monthly_cashflow['calendar_month'] == month_temp, 'electricity_bill_after_slp'] = (temp_bill_after_lighting - temp_bill_after_slp)

    df_monthly_cashflow['electricity_bill_original'] = df_monthly_cashflow['electricity_bill_original']*df_monthly_cashflow['escalations_multiplier']
    df_monthly_cashflow['electricity_bill_after_lighting'] = df_monthly_cashflow['electricity_bill_original'] - (df_monthly_cashflow['electricity_bill_original'] - df_monthly_cashflow['electricity_bill_after_lighting']*df_monthly_cashflow['escalations_multiplier']) * (1-df_lighting_degradation_cashflow['total_cummulative_loss'])


    if df_monthly_cashflow['solar_generation_ideal'].sum() > 0:
        df_monthly_cashflow['electricity_bill_after_slp'] = df_monthly_cashflow['electricity_bill_after_lighting'] - df_monthly_cashflow['electricity_bill_after_slp']*df_monthly_cashflow['escalations_multiplier']*df_monthly_cashflow['solar_generation_utilised']
    else:
        df_monthly_cashflow['electricity_bill_after_slp'] = df_monthly_cashflow['electricity_bill_after_lighting'] - df_monthly_cashflow['electricity_bill_after_slp']*df_monthly_cashflow['escalations_multiplier']


    # ----------------------Lighting Savings-------------------------------------------
    df_monthly_cashflow['lighting_bill_savings'] = df_monthly_cashflow['electricity_bill_original'] - df_monthly_cashflow['electricity_bill_after_lighting']
    df_monthly_cashflow['lighting_volume_savings'] = df_monthly_cashflow['lighting_bill_savings'] * df_monthly_cashflow['lighting_energy_savings_proportion']
    df_monthly_cashflow['lighting_demand_savings'] = df_monthly_cashflow['lighting_bill_savings'] - df_monthly_cashflow['lighting_volume_savings']
    df_monthly_cashflow['lighting_maintenance_savings'] = df_lighting_degradation_cashflow['total_maintenance_savings']
    df_monthly_cashflow['total_lighting_savings'] = df_monthly_cashflow['lighting_maintenance_savings'] + df_monthly_cashflow['lighting_bill_savings']

    # ----------------------Solar and PFC Savings-------------------------------------------
    df_monthly_cashflow['solarpfc_bill_savings'] = df_monthly_cashflow['electricity_bill_after_lighting'] - df_monthly_cashflow['electricity_bill_after_slp']
    df_monthly_cashflow['solarpfc_volume_savings'] = df_monthly_cashflow['solarpfc_bill_savings'] * df_monthly_cashflow['solarpfc_energy_savings_proportion']
    df_monthly_cashflow['solarpfc_demand_savings'] = df_monthly_cashflow['solarpfc_bill_savings'] - df_monthly_cashflow['solarpfc_volume_savings']
    df_monthly_cashflow['LGC_utilised'] = df_monthly_cashflow['LGC_price'] * df_monthly_cashflow['solar_generation_utilised'] * lgc_flag/ 1000
    df_monthly_cashflow['LGC_spill'] = df_monthly_cashflow['LGC_price'] * df_monthly_cashflow['solar_generation_spill'] * lgc_flag / 1000
    df_monthly_cashflow['feed_in_income'] = df_monthly_cashflow['solar_generation_spill'] * df_monthly_cashflow['Feed_in_rates']
    df_monthly_cashflow['total_solarpfc_savings'] = df_monthly_cashflow['solarpfc_bill_savings'] + df_monthly_cashflow['LGC_utilised'] + df_monthly_cashflow['LGC_spill'] + df_monthly_cashflow['feed_in_income']

    #----------------------Total Savings------------------------------------------------------
    df_monthly_cashflow['total_bill_savings'] = df_monthly_cashflow['solarpfc_bill_savings'] + df_monthly_cashflow['lighting_bill_savings']
    df_monthly_cashflow['LGCs'] = df_monthly_cashflow['LGC_utilised'] + df_monthly_cashflow['LGC_spill']
    df_monthly_cashflow['total_savings'] = df_monthly_cashflow['total_bill_savings'] + df_monthly_cashflow['LGCs'] + df_monthly_cashflow['lighting_maintenance_savings'] + df_monthly_cashflow['feed_in_income']

    # ----------------------------Net Cashflows--------------------------------------------
    df_monthly_cashflow['net_cashflows'] = df_monthly_cashflow['total_savings']

    # ---------------------------- Calendar Year Cashflow --------------------------------------------
    df_calendar_year_cashflow = df_monthly_cashflow.groupby(['calendar_year']).sum()
    df_calendar_year_cashflow.drop(['calendar_month','system_month','system_year','panel_performance','escalations_multiplier','LGC_price','Feed_in_rates'],axis=1, inplace=True)
    df_calendar_year_cashflow.drop(['lighting_energy_savings_proportion','solarpfc_energy_savings_proportion'], axis=1, inplace=True)
    df_calendar_year_cashflow = df_calendar_year_cashflow.astype('float64')

    # ---------------------------- System Year Cashflow --------------------------------------------
    df_system_year_cashflow = df_monthly_cashflow.groupby(['system_year']).sum()
    df_system_year_cashflow.drop(['calendar_month','system_month','calendar_year','panel_performance','escalations_multiplier','LGC_price','Feed_in_rates'],axis=1, inplace=True)
    df_system_year_cashflow.drop(['lighting_energy_savings_proportion','solarpfc_energy_savings_proportion'], axis=1, inplace=True)
    df_system_year_cashflow = df_system_year_cashflow.astype('float64')

    return df_monthly_cashflow, df_system_year_cashflow, df_calendar_year_cashflow


def calculate_capex_metrics(df_system_year_cashflow, input_data_dict):
    # Solar, PFC and Lighting Capex
    discount_rate = float(input_data_dict['program_overrides_dict']['discount_rate']) / 100
    lighting_boolean = input_data_dict['lighting_boolean']
    
    if lighting_boolean == 1:
        lighting_cost = float(input_data_dict['lighting_output_dict']['total_cost'])
        verdia_lighting_fee_dollars = float(input_data_dict['lighting_output_dict']['verdia_fee_dollars'])
    else:
        lighting_cost = 0
        verdia_lighting_fee_dollars = 0

    solar_cost = float(input_data_dict['solar_price_dict']['system_cost'])
    stc_discount = float(input_data_dict['solar_price_dict']['stc_discount'])
    verdia_solar_fee_dollars = float(input_data_dict['solar_price_dict']['verdia_fee_dollars'])
    
    pfc_cost = float(input_data_dict['pfc_price_dict']['system_cost'])
    verdia_pfc_fee_dollars = float(input_data_dict['pfc_price_dict']['verdia_fee_dollars'])
    
    total_cost = lighting_cost + solar_cost + pfc_cost
    total_verdia_fee_dollars = verdia_lighting_fee_dollars + verdia_solar_fee_dollars + verdia_pfc_fee_dollars

    # print(f"total cost = {lighting_cost} + {solar_cost} + {pfc_cost} = {total_cost}")

    net_cashflows = np.zeros(len(df_system_year_cashflow.index)+1,)
    cum_cashflows = np.zeros(len(df_system_year_cashflow.index)+1,)
    net_cashflows[0] = -total_cost
    cum_cashflows[0] = -total_cost
    Payback = 25
    for i in range(len(df_system_year_cashflow.index)):
        current_val = df_system_year_cashflow['net_cashflows'].values[i]
        net_cashflows[i+1] = current_val
        cum_cashflows[i+1] = cum_cashflows[i] + current_val
        if cum_cashflows[i+1]>=0 and cum_cashflows[i]<0:
            Payback = np.around(i - (cum_cashflows[i] / (cum_cashflows[i+1] - cum_cashflows[i])),2)

    
    LCOE_calcs = np.zeros((len(df_system_year_cashflow.index)+1,6))
    
    for i in range(len(df_system_year_cashflow.index)+1):
        if i==0:
            LCOE_calcs[i,0] = -solar_cost
            LCOE_calcs[i,1] = -solar_cost
            LCOE_calcs[i,2] = 0
        else:
            LCOE_calcs[i,0] = 0
            LCOE_calcs[i,1] = df_system_year_cashflow['LGCs'].values[i-1]
            LCOE_calcs[i,2] = (df_system_year_cashflow['solar_generation_utilised'] + df_system_year_cashflow['solar_generation_spill']).values[i-1]
        LCOE_calcs[i,3] = (1 + discount_rate)**i
        LCOE_calcs[i,4] = LCOE_calcs[i,1] / LCOE_calcs[i,3]
        LCOE_calcs[i,5] = LCOE_calcs[i,2] / LCOE_calcs[i,3]

    # print(pd.DataFrame(data=LCOE_calcs))
    NPV = round(np.npv(discount_rate, net_cashflows[:21]),2)
    IRRs = round(np.irr(net_cashflows[:21]),4)
    # print(IRRs)
    if np.isnan(IRRs):
        IRRs = 0.0
    
    LCOE = -round(sum(LCOE_calcs[0:21,4]) / sum(LCOE_calcs[0:21,5]),4)
    if np.isnan(LCOE):
        LCOE = 0.0

    Simplified_LCOE = -round(sum(LCOE_calcs[0:21,0]) / sum(LCOE_calcs[0:21,2]),4)
    if np.isnan(Simplified_LCOE):
        Simplified_LCOE = 0.0

    data = {
        'NPV': NPV,
        'IRR': IRRs,
        'LCOE': LCOE,
        'payback': Payback,
        'Simplified_LCOE': Simplified_LCOE,
        'total_cost': total_cost,
        'total_verdia_fee_dollars': total_verdia_fee_dollars,
        'ten_year_savings': np.sum(cum_cashflows[0:11])
    }

    return data


def calculate_summary_params(df_monthly_load_summary, df_system_year_cashflow, df_monthly_bill_summary, input_data_dict):
    # Summary parameters
    output_summary_dict = {}
    
    output_summary_dict['solar_size'] = float(input_data_dict['solar_price_dict']['solar_size'])
    output_summary_dict['pfc_size'] = float(input_data_dict['pfc_price_dict']['pfc_size'])

    lighting_boolean = input_data_dict['lighting_boolean']

   
    if lighting_boolean == 1:
        output_summary_dict['lighting_cost'] = float(input_data_dict['lighting_output_dict']['total_cost'])
        output_summary_dict['verdia_lighting_fee_dollars'] = float(input_data_dict['lighting_output_dict']['verdia_fee_dollars'])
        output_summary_dict['num_led_lights'] = input_data_dict['lighting_output_dict']['number_of_lights']
    else:
        output_summary_dict['lighting_cost'] = 0
        output_summary_dict['verdia_lighting_fee_dollars'] = 0
        output_summary_dict['num_led_lights'] = 0

    output_summary_dict['solar_cost'] = float(input_data_dict['solar_price_dict']['system_cost'])
    output_summary_dict['stc_discount'] = float(input_data_dict['solar_price_dict']['stc_discount'])
    output_summary_dict['verdia_solar_fee_dollars'] = float(input_data_dict['solar_price_dict']['verdia_fee_dollars'])
    
    output_summary_dict['pfc_cost'] = float(input_data_dict['pfc_price_dict']['system_cost'])
    output_summary_dict['verdia_pfc_fee_dollars'] = float(input_data_dict['pfc_price_dict']['verdia_fee_dollars'])

    output_summary_dict['total_cost'] = output_summary_dict['lighting_cost'] + output_summary_dict['solar_cost'] + output_summary_dict['pfc_cost']
    output_summary_dict['total_verdia_fee_dollars'] = output_summary_dict['verdia_lighting_fee_dollars'] + \
                            output_summary_dict['verdia_solar_fee_dollars'] + output_summary_dict['verdia_pfc_fee_dollars']

    try:
        output_summary_dict['load_consumption'] = df_monthly_load_summary['original_kwhs'].sum() / 1000
        output_summary_dict['load_after_system'] = df_monthly_load_summary['after_slp_kwhs'].sum() / 1000
        output_summary_dict['load_reduction'] = output_summary_dict['load_consumption'] - output_summary_dict['load_after_system']
        output_summary_dict['load_reduction_percent'] = (output_summary_dict['load_reduction'] / output_summary_dict['load_consumption'])*100
        output_summary_dict['greenhouse_reduction'] = 165

        output_summary_dict['bill_savings_1st_year'] = df_system_year_cashflow['total_bill_savings'][1]
        output_summary_dict['LGCs_1st_year'] = df_system_year_cashflow['LGCs'][1]
        output_summary_dict['lighting_maintenance_savings_1st_year'] = df_system_year_cashflow['lighting_maintenance_savings'][1]    
        output_summary_dict['feed_in_income_1st_year'] = df_system_year_cashflow['feed_in_income'][1]
        output_summary_dict['net_savings_1st_year'] = df_system_year_cashflow['total_savings'][1]

        output_summary_dict['electricity_current_bill'] = (df_monthly_bill_summary['original_volume_charges'] + df_monthly_bill_summary['original_demand_charges'] + df_monthly_bill_summary['fixed_charges']).sum()
        output_summary_dict['electricity_bill_1st_year'] =  df_system_year_cashflow['electricity_bill_original'][1]
        output_summary_dict['electricity_bill_after_system_1st_year'] =  df_system_year_cashflow['electricity_bill_after_slp'][1]
        output_summary_dict['electricity_bill_reduction_percent_1st_year'] =  (output_summary_dict['electricity_bill_1st_year'] - output_summary_dict['electricity_bill_after_system_1st_year'])/output_summary_dict['electricity_bill_1st_year']
        output_summary_dict['electricity_cost_reduction_percent_1st_year'] =  output_summary_dict['net_savings_1st_year']/output_summary_dict['electricity_bill_1st_year']

        output_summary_dict['lighting_load_reduction_1st_year'] = df_system_year_cashflow['lighting_load_reduction'][1]
        output_summary_dict['lighting_load_reduction_percent_1st_year'] = output_summary_dict['lighting_load_reduction_1st_year'] / (output_summary_dict['load_consumption']*1000)
        output_summary_dict['lighting_bill_savings_1st_year'] = df_system_year_cashflow['lighting_bill_savings'][1]
        output_summary_dict['lighting_total_savings_1st_year'] = df_system_year_cashflow['total_lighting_savings'][1]
        if output_summary_dict['lighting_total_savings_1st_year'] == 0:
            output_summary_dict['lighting_simple_payback'] = 25
        else:
            output_summary_dict['lighting_simple_payback'] = output_summary_dict['lighting_cost'] / output_summary_dict['lighting_total_savings_1st_year']

        output_summary_dict['solar_generation_ideal_1st_year'] = df_system_year_cashflow['solar_generation_ideal'][1]
        output_summary_dict['solar_generation_utilised_1st_year'] = df_system_year_cashflow['solar_generation_utilised'][1]
        if output_summary_dict['solar_generation_ideal_1st_year'] == 0:
            output_summary_dict['solar_utilisation_percent'] = 1 
        else:
            output_summary_dict['solar_utilisation_percent'] = output_summary_dict['solar_generation_utilised_1st_year'] / output_summary_dict['solar_generation_ideal_1st_year']
        output_summary_dict['solar_load_reduction_1st_year'] = output_summary_dict['solar_generation_utilised_1st_year']
        output_summary_dict['solar_load_reduction_percent_1st_year'] = output_summary_dict['solar_generation_utilised_1st_year'] / (output_summary_dict['load_consumption']*1000)
        output_summary_dict['solar_exported_1st_year'] = df_system_year_cashflow['solar_generation_spill'][1]
        output_summary_dict['solar_bill_savings_1st_year'] = df_system_year_cashflow['solarpfc_bill_savings'][1]
        output_summary_dict['peak_power_factor_before'] = df_monthly_load_summary['after_lighting_kw'].mean() / df_monthly_load_summary['after_lighting_kva'].mean()
        output_summary_dict['peak_power_factor_after'] = df_monthly_load_summary['after_slp_kw'].mean() / df_monthly_load_summary['after_slp_kva'].mean()

        if df_system_year_cashflow['total_solarpfc_savings'][1] == 0:
            output_summary_dict['solarpfc_simple_payback'] = 25
        else:
            output_summary_dict['solarpfc_simple_payback'] = (output_summary_dict['solar_cost'] + output_summary_dict['pfc_cost'])/df_system_year_cashflow['total_solarpfc_savings'][1]

        output_summary_dict['blended_rate'] = output_summary_dict['electricity_current_bill']/(output_summary_dict['load_consumption']*1000)

        if output_summary_dict['solar_generation_utilised_1st_year'] == 0:
            output_summary_dict['solarpfc_savings_rate'] = 0
        else:
            output_summary_dict['solarpfc_savings_rate'] = output_summary_dict['solar_bill_savings_1st_year'] / output_summary_dict['solar_generation_utilised_1st_year']

        if df_system_year_cashflow['lighting_bill_savings'][1] == 0:
            output_summary_dict['lighting_energy_savings_proportion'] = 1
        else:
            output_summary_dict['lighting_energy_savings_proportion'] = df_system_year_cashflow['lighting_volume_savings'][1] / df_system_year_cashflow['lighting_bill_savings'][1]

        if df_system_year_cashflow['solarpfc_bill_savings'][1] == 0:
            output_summary_dict['solarpfc_energy_savings_proportion'] = 1
        else:
            output_summary_dict['solarpfc_energy_savings_proportion'] = df_system_year_cashflow['solarpfc_volume_savings'][1] / df_system_year_cashflow['solarpfc_bill_savings'][1]
        
        if df_system_year_cashflow['total_bill_savings'][1] == 0:
            output_summary_dict['total_energy_savings_proportion'] = 1
        else:
            output_summary_dict['total_energy_savings_proportion'] = (df_system_year_cashflow['lighting_volume_savings'][1] + df_system_year_cashflow['solarpfc_volume_savings'][1]) / df_system_year_cashflow['total_bill_savings'][1]
        
        if output_summary_dict['solar_generation_utilised_1st_year'] == 0:
            output_summary_dict['solarpfc_energy_savings_rate'] = 0
        else:
            output_summary_dict['solarpfc_energy_savings_rate'] = df_system_year_cashflow['solarpfc_volume_savings'][1] / output_summary_dict['solar_generation_utilised_1st_year']
    
    except Exception as e:
        return str(e)

    return output_summary_dict


def add_solar_data_iterations(df, input_data_dict, solar_size):

    solar_df = pd.DataFrame(input_data_dict['solar_data_datetime'], columns=['Datetime'])
    solar_df['kW'] = input_data_dict['solar_data_kW']

    # Interpolate Solar kW
    solar_df['real_date'] = pd.TimedeltaIndex(
        solar_df['Datetime'], unit='d') + dt.datetime(1899, 12, 30)
    # rounding to nearest hour
    solar_df['rounded_date'] = solar_df['real_date'].dt.round('60min')
    
    
    solar_df_2 = pd.DataFrame()
    solar_df_2['rounded_date'] = pd.date_range(start='1/1/2001 00:30', end='1/1/2002 00:00', freq='0.5H')   
    solar_df_2['month'] = pd.DatetimeIndex(solar_df_2['rounded_date']).month
    solar_df_2 = pd.merge(solar_df_2,solar_df,how='outer',on='rounded_date')
    solar_df_2['original_solar'] = solar_df_2['kW']
    solar_df_2['kW'] = solar_df_2['kW'].interpolate()    
    # print(f"Sum kWh : {solar_df_2['kW'][solar_df_2['kW']>0].sum()/2} vs {solar_df['kW'].sum()}")
    solar_df_2['kW'].fillna(0,inplace=True) 

    solar_poe = 95
    solar_perc = []
    solar_perc_monthly = np.zeros((12,48))
    months = solar_df_2['month'].to_numpy().reshape(365,48)
    months = months[:,1]
    solar_kW = solar_df_2['kW'].to_numpy().reshape(365,48)
    total_length = 0
    for i in range(1,13):
        temp_solar_kW = solar_kW[months==i,:]
        len_month = temp_solar_kW.shape[0]
        temp_solar_perc = np.percentile(temp_solar_kW, 100-solar_poe ,axis = 0)
        solar_perc_monthly[i-1,:] = temp_solar_perc
        solar_perc = np.concatenate((solar_perc, np.tile(temp_solar_perc,len_month)))
        total_length = total_length + len_month*48

    df['solar_kW'] = solar_df_2['kW']*solar_size/100
    df['solar_kW_POE'] = solar_perc*solar_size/100

    return df


def calculate_capex_metrics_iterations(df_system_year_cashflow, input_data_dict, solar_size):
    # Solar, PFC and Lighting Capex
    
    if input_data_dict['lighting_boolean'] == 1:
        lighting_cost = float(input_data_dict['lighting_output_dict']['total_cost'])
    else:
        lighting_cost = 0
    
    #------------------------------------------------------ Solar Cost -------------------------------

    # Calculating Solar Unit Cost
        
    solar_cost_dict = input_data_dict['solar_cost_dict']
    for solar_cost in solar_cost_dict:
        if solar_size <= float(solar_cost['system_size']):
            solar_unit_cost = float(solar_cost['multi_site_dollar_per_watt'])
            solar_verdia_fee = float(solar_cost['multi_site_verdia_fee'])
            break
    
    solar_unit_cost_override = input_data_dict['solar_price_dict']['solar_unit_cost_override']
    
    if solar_unit_cost_override != "" and solar_unit_cost_override is not None :
        solar_unit_cost_override = float(solar_unit_cost_override)
        solar_unit_cost = solar_unit_cost_override

    
    gross_system_cost = round(solar_size*solar_unit_cost*1000,2)
    other_adjustments_1 = float(input_data_dict['solar_price_dict']['other_adjustments_1'])
    other_adjustments_2 = float(input_data_dict['solar_price_dict']['other_adjustments_2'])
    verdia_fee = float(input_data_dict['solar_price_dict']['verdia_fee'])            
    verdia_fee_dollars = (gross_system_cost + other_adjustments_1)*(verdia_fee)/100

    system_type_override = input_data_dict['solar_price_dict']['system_type_override']
    if system_type_override == "No override":
        if solar_size > 100:
            system_type = "LGC"
        else:
            system_type = "STC"
    else:
        system_type = system_type_override
           
    stc_deeming_period = float(input_data_dict['solar_price_dict']['stc_deeming_period'])
    stc_price = float(input_data_dict['certificate_prices_dict']['STCprice'])            
    rating = float(input_data_dict['postcode_resource_dict']['rating'])
    
    if system_type == "STC":
        stc_discount = round(solar_size*stc_deeming_period*stc_price*rating,2)
    else:
        stc_discount = 0

    solar_cost = round(gross_system_cost+ other_adjustments_1 + verdia_fee_dollars+ other_adjustments_2 - stc_discount,2)
    # print(f'{gross_system_cost},{other_adjustments_1},{verdia_fee_dollars},{other_adjustments_2},{stc_discount}')


    pfc_cost = float(input_data_dict['pfc_price_dict']['system_cost'])

    total_cost = lighting_cost + solar_cost + pfc_cost

    # print(f"total cost = {lighting_cost} + {solar_cost} + {pfc_cost} = {total_cost}")

    net_cashflows = np.zeros(len(df_system_year_cashflow.index)+1,)
    cum_cashflows = np.zeros(len(df_system_year_cashflow.index)+1,)
    net_cashflows[0] = -total_cost
    cum_cashflows[0] = -total_cost
    Payback = 25
    for i in range(len(df_system_year_cashflow.index)):
        current_val = df_system_year_cashflow['net_cashflows'].values[i]
        net_cashflows[i+1] = current_val
        cum_cashflows[i+1] = cum_cashflows[i] + current_val
        if cum_cashflows[i+1]>=0 and cum_cashflows[i]<0:
            Payback = np.around(i - (cum_cashflows[i] / (cum_cashflows[i+1] - cum_cashflows[i])),2)

    
    LCOE_calcs = np.zeros((len(df_system_year_cashflow.index)+1,6))
    discount_rate = input_data_dict['program_overrides_dict']['discount_rate']

    for i in range(len(df_system_year_cashflow.index)+1):
        if i==0:
            LCOE_calcs[i,0] = -solar_cost
            LCOE_calcs[i,1] = -solar_cost
            LCOE_calcs[i,2] = 0
        else:
            LCOE_calcs[i,0] = 0
            LCOE_calcs[i,1] = df_system_year_cashflow['LGCs'].values[i-1]
            LCOE_calcs[i,2] = (df_system_year_cashflow['solar_generation_utilised'] + df_system_year_cashflow['solar_generation_spill']).values[i-1]
        LCOE_calcs[i,3] = (1 + discount_rate)**i
        LCOE_calcs[i,4] = LCOE_calcs[i,1] / LCOE_calcs[i,3]
        LCOE_calcs[i,5] = LCOE_calcs[i,2] / LCOE_calcs[i,3]

    # print(pd.DataFrame(data=LCOE_calcs))
    NPV = round(np.npv(discount_rate, net_cashflows[:21]),2)
    IRR = round(np.irr(net_cashflows[:21]),4)
    LCOE = -round(sum(LCOE_calcs[0:21,4]) / sum(LCOE_calcs[0:21,5]),4)
    
    data = {
        'NPV': NPV,
        'IRR': IRR,
        'LCOE': LCOE,
        'payback': Payback,
        'total_cost': total_cost,
        'stc_discount':stc_discount,
        'lighting_cost': lighting_cost,
        'solar_cost': solar_cost,
        'pfc_cost': pfc_cost,
        'ten_year_savings': np.sum(net_cashflows[0:11])

    }

    return data


def calculate_capex_metrics_program(df_system_year_cashflow, program_summary_dict):
    capex_metrics_dict = {}
    # Hardcoded -- to be changed
    discount_rate = program_summary_dict['discount_rate'] / 100
    
    net_cashflows = np.zeros(len(df_system_year_cashflow.index)+1,)
    cum_cashflows = np.zeros(len(df_system_year_cashflow.index)+1,)
    net_cashflows[0] = -program_summary_dict['total_cost']
    cum_cashflows[0] = -program_summary_dict['total_cost']
    payback = 25

    for i in range(len(df_system_year_cashflow.index)):
        current_val = df_system_year_cashflow['net_cashflows'].values[i]
        net_cashflows[i+1] = current_val
        cum_cashflows[i+1] = cum_cashflows[i] + current_val
        if cum_cashflows[i+1]>=0 and cum_cashflows[i]<0:
            payback = np.around(i - (cum_cashflows[i] / (cum_cashflows[i+1] - cum_cashflows[i])),2)

    

    LCOE_calcs = np.zeros((len(df_system_year_cashflow.index)+1,6))    

    for i in range(len(df_system_year_cashflow.index)+1):
        if i==0:
            LCOE_calcs[i,0] = -program_summary_dict['solar_cost']
            LCOE_calcs[i,1] = -program_summary_dict['solar_cost']
            LCOE_calcs[i,2] = 0
        else:
            LCOE_calcs[i,0] = 0
            LCOE_calcs[i,1] = df_system_year_cashflow['LGCs'].values[i-1]
            LCOE_calcs[i,2] = (df_system_year_cashflow['solar_generation_utilised'] + df_system_year_cashflow['solar_generation_spill']).values[i-1]
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

    print(f'NPV = {NPV}')
    print(f'IRR = {IRRs}')
    print(f'LCOE = {LCOE}')
    print(f'Simplified_LCOE = {Simplified_LCOE}')
    print(f'Payback = {payback}')

    capex_metrics_dict['payback'] = payback
    capex_metrics_dict['NPV'] = NPV
    capex_metrics_dict['IRR'] = IRRs
    capex_metrics_dict['LCOE'] = LCOE
    capex_metrics_dict['Simplified_LCOE'] = Simplified_LCOE
    capex_metrics_dict['total_cost'] = program_summary_dict['total_cost']

    return capex_metrics_dict


def calculate_summary_params_program(df_monthly_load_summary, df_system_year_cashflow, output_summary_dict):
    
    output_summary_dict['load_consumption'] = df_monthly_load_summary['original_kwhs'].sum() / 1000
    output_summary_dict['load_after_system'] = df_monthly_load_summary['after_slp_kwhs'].sum() / 1000
    output_summary_dict['load_reduction'] = output_summary_dict['load_consumption'] - output_summary_dict['load_after_system']
    output_summary_dict['load_reduction_percent'] = (output_summary_dict['load_reduction'] / output_summary_dict['load_consumption'])*100
    output_summary_dict['greenhouse_reduction'] = 165

    output_summary_dict['bill_savings_1st_year'] = df_system_year_cashflow['total_bill_savings'][1]
    output_summary_dict['LGCs_1st_year'] = df_system_year_cashflow['LGCs'][1]
    output_summary_dict['lighting_maintenance_savings_1st_year'] = df_system_year_cashflow['lighting_maintenance_savings'][1]    
    output_summary_dict['feed_in_income_1st_year'] = df_system_year_cashflow['feed_in_income'][1]
    output_summary_dict['net_savings_1st_year'] = df_system_year_cashflow['total_savings'][1]

    output_summary_dict['electricity_bill_1st_year'] =  df_system_year_cashflow['electricity_bill_original'][1]
    output_summary_dict['electricity_bill_after_system_1st_year'] =  df_system_year_cashflow['electricity_bill_after_slp'][1]
    output_summary_dict['electricity_bill_reduction_percent_1st_year'] =  (output_summary_dict['electricity_bill_1st_year'] - output_summary_dict['electricity_bill_after_system_1st_year'])/output_summary_dict['electricity_bill_1st_year']
    output_summary_dict['electricity_cost_reduction_percent_1st_year'] =  output_summary_dict['net_savings_1st_year']/output_summary_dict['electricity_bill_1st_year']

    output_summary_dict['lighting_load_reduction_1st_year'] = df_system_year_cashflow['lighting_load_reduction'][1]
    output_summary_dict['lighting_load_reduction_percent_1st_year'] = output_summary_dict['lighting_load_reduction_1st_year'] / (output_summary_dict['load_consumption']*1000)
    output_summary_dict['lighting_bill_savings_1st_year'] = df_system_year_cashflow['lighting_bill_savings'][1]
    output_summary_dict['lighting_total_savings_1st_year'] = df_system_year_cashflow['total_lighting_savings'][1]
    if output_summary_dict['lighting_total_savings_1st_year'] == 0:
        output_summary_dict['lighting_simple_payback'] = 25
    else:
        output_summary_dict['lighting_simple_payback'] = output_summary_dict['lighting_cost'] / output_summary_dict['lighting_total_savings_1st_year']

    output_summary_dict['solar_generation_ideal_1st_year'] = df_system_year_cashflow['solar_generation_ideal'][1]
    output_summary_dict['solar_generation_utilised_1st_year'] = df_system_year_cashflow['solar_generation_utilised'][1]
    if output_summary_dict['solar_generation_ideal_1st_year'] == 0:
        output_summary_dict['solar_utilisation_percent'] = 1 
    else:
        output_summary_dict['solar_utilisation_percent'] = output_summary_dict['solar_generation_utilised_1st_year'] / output_summary_dict['solar_generation_ideal_1st_year']

    output_summary_dict['solar_load_reduction_1st_year'] = output_summary_dict['solar_generation_utilised_1st_year']
    output_summary_dict['solar_load_reduction_percent_1st_year'] = output_summary_dict['solar_generation_utilised_1st_year'] / (output_summary_dict['load_consumption']*1000)
    output_summary_dict['solar_exported_1st_year'] = df_system_year_cashflow['solar_generation_spill'][1]
    output_summary_dict['solar_bill_savings_1st_year'] = df_system_year_cashflow['solarpfc_bill_savings'][1]
    

    if df_system_year_cashflow['total_solarpfc_savings'][1] == 0:
        output_summary_dict['solarpfc_simple_payback'] = 25
    else:
        output_summary_dict['solarpfc_simple_payback'] = (output_summary_dict['solar_cost'] + output_summary_dict['pfc_cost'])/df_system_year_cashflow['total_solarpfc_savings'][1]

    # output_summary_dict['blended_rate'] = output_summary_dict['electricity_current_bill']/(output_summary_dict['load_consumption']*1000)

    if output_summary_dict['solar_generation_utilised_1st_year'] == 0:
        output_summary_dict['solarpfc_savings_rate'] = 0
    else:
        output_summary_dict['solarpfc_savings_rate'] = output_summary_dict['solar_bill_savings_1st_year'] / output_summary_dict['solar_generation_utilised_1st_year']

    if df_system_year_cashflow['lighting_bill_savings'][1] == 0:
        output_summary_dict['lighting_energy_savings_proportion'] = 1
    else:
        output_summary_dict['lighting_energy_savings_proportion'] = df_system_year_cashflow['lighting_volume_savings'][1] / df_system_year_cashflow['lighting_bill_savings'][1]

    if df_system_year_cashflow['solarpfc_bill_savings'][1] == 0:
        output_summary_dict['solarpfc_energy_savings_proportion'] = 1
    else:
        output_summary_dict['solarpfc_energy_savings_proportion'] = df_system_year_cashflow['solarpfc_volume_savings'][1] / df_system_year_cashflow['solarpfc_bill_savings'][1]
    
    if df_system_year_cashflow['total_bill_savings'][1] == 0:
        output_summary_dict['total_energy_savings_proportion'] = 1
    else:
        output_summary_dict['total_energy_savings_proportion'] = (df_system_year_cashflow['lighting_volume_savings'][1] + df_system_year_cashflow['solarpfc_volume_savings'][1]) / df_system_year_cashflow['total_bill_savings'][1]
    
    if output_summary_dict['solar_generation_utilised_1st_year'] == 0:
        output_summary_dict['solarpfc_energy_savings_rate'] = 0
    else:
        output_summary_dict['solarpfc_energy_savings_rate'] = df_system_year_cashflow['solarpfc_volume_savings'][1] / output_summary_dict['solar_generation_utilised_1st_year']
    
    return output_summary_dict