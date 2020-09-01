from django.shortcuts import render, get_object_or_404
from .models import Scenario, IntervalData
from .forms import IntervalDataForm
from inputs.forms import (BillDetailForm, OperatingHourDetailForm, HolidayDetailForm, PriceForecastOverrideForm,
                          EscalationsOverrideForm, SolarExportForm)
from inputs.models import (BillDetail, OperatingHourDetail, HolidayDetail, PriceForecastOverride, EscalationsOverride,
                           SolarExport)
from powerbillinputs.models import (EnergyCharge, DemandCharge, FixedCharge)
from powerbillinputs.forms import (EnergyChargeForm, DemandChargeForm, FixedChargeForm)
from powerbillinputs.serializers import (EnergyChargeSerializer, DemandChargeSerializer, FixedChargeSerializer)
from lighting.forms import LightingHourDetailForm, LightingInputForm, LightingOutputForm
from lighting.models import LightingHourDetail, LightingOutput

from references.models import TariffEscalations
from solarpfc.forms import SolarLayoutForm, SolarPriceForm, PFCPriceForm
from solarpfc.models import SolarLayout, SolarPrice, PFCPrice
from simulations.models import SimulationParameter
from simulations.forms import SimulationParameterForm
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url="/")
def main_scenario_page(request):
    scenario_id = request.POST['hidden_scenario_id']
    scenario = get_object_or_404(Scenario, id=scenario_id)
    print(scenario_id)
    bill_detail = BillDetail.objects.all().filter(scenario=scenario).first()
    operating_hour_detail = OperatingHourDetail.objects.all().filter(
        scenario=scenario).first()
    holiday_detail = HolidayDetail.objects.all().filter(scenario=scenario).first()
    price_forecast_override = PriceForecastOverride.objects.all().filter(
        scenario=scenario).first()
    escalations_override = EscalationsOverride.objects.all().filter(
        scenario=scenario).first()
    solar_export = SolarExport.objects.all().filter(
        scenario=scenario).first()

    if not bill_detail:
        bill_detail_form = BillDetailForm()
    else:
        bill_detail_form = BillDetailForm(instance=bill_detail)

    if not operating_hour_detail:
        operating_hour_detail_form = OperatingHourDetailForm()
    else:
        operating_hour_detail_form = OperatingHourDetailForm(
            instance=operating_hour_detail)

    if not holiday_detail:
        holiday_detail_form = HolidayDetailForm()
    else:
        holiday_detail_form = HolidayDetailForm(instance=holiday_detail)

    if not price_forecast_override:
        price_forecast_override_form = PriceForecastOverrideForm()
    else:
        price_forecast_override_form = PriceForecastOverrideForm(
            instance=price_forecast_override)

    if not escalations_override:
        escalations_override_form = EscalationsOverrideForm()
    else:
        escalations_override_form = EscalationsOverrideForm(
            instance=escalations_override)
    
    if not solar_export:
        solar_export_form = SolarExportForm()
    else:
        solar_export_form = SolarExportForm(
            instance=solar_export)

    lighting_input_form = LightingInputForm()
    lighting_input_form.fields['lighting_type'].queryset = LightingHourDetail.objects.all().filter(scenario=scenario)

    lighting_output = LightingOutput.objects.all().filter(scenario=scenario).first()
    if not lighting_output:
        lighting_output_form = LightingOutputForm()
    else:
        lighting_output_form = LightingOutputForm(instance=lighting_output)

    solar_layout = SolarLayout.objects.all().filter(scenario=scenario).first()
    if not solar_layout:
        solar_layout_url = ""
    else:
        solar_layout_url = solar_layout.solar_layout_file.url

    solar_price = SolarPrice.objects.all().filter(scenario=scenario).first()
    if not solar_price:
        solar_price_form = SolarPriceForm()
    else:
        solar_price_form = SolarPriceForm(instance=solar_price)

    pfc_price = PFCPrice.objects.all().filter(scenario=scenario).first()
    if not pfc_price:
        pfc_price_form = PFCPriceForm()
    else:
        pfc_price_form = PFCPriceForm(instance=pfc_price)

    simulation_parameter = SimulationParameter.objects.all().filter(scenario=scenario).first()
    if not simulation_parameter:
        simulation_parameter_form  = SimulationParameterForm()
    else:
        simulation_parameter_form  = SimulationParameterForm(instance=simulation_parameter)
    simulation_parameter_form.fields["interval_data"].queryset = IntervalData.objects.all().filter(scenario=scenario)




    context = {
        'scenario': scenario,
        'bill_detail_form': bill_detail_form,
        'operating_hour_detail_form': operating_hour_detail_form,
        'holiday_detail_form': holiday_detail_form,
        'price_forecast_override_form': price_forecast_override_form,
        'tariff_escalations_2019': getattr(TariffEscalations.objects.filter(year=2019).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2020': getattr(TariffEscalations.objects.filter(year=2020).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2021': getattr(TariffEscalations.objects.filter(year=2021).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2022': getattr(TariffEscalations.objects.filter(year=2022).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2023': getattr(TariffEscalations.objects.filter(year=2023).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2024': getattr(TariffEscalations.objects.filter(year=2024).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2025': getattr(TariffEscalations.objects.filter(year=2025).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2026': getattr(TariffEscalations.objects.filter(year=2026).first(), scenario.site_name.state.lower()),
        'tariff_escalations_2027': getattr(TariffEscalations.objects.filter(year=2027).first(), scenario.site_name.state.lower()),
        'escalations_override_form': escalations_override_form,
        'solar_export_form': solar_export_form,
        'energy_charge_form': EnergyChargeForm(),
        'demand_charge_form': DemandChargeForm(),
        'fixed_charge_form': FixedChargeForm(),
        'interval_data_form': IntervalDataForm(),
        'lighting_hour_detail_form': LightingHourDetailForm(),
        'lighting_input_form' : lighting_input_form,
        'lighting_output_form' : lighting_output_form,
        'solar_layout_form' : SolarLayoutForm,
        'solar_layout_url' : solar_layout_url,
        'solar_price_form' : solar_price_form,
        'pfc_price_form' : pfc_price_form,
        'simulation_parameter_form' : simulation_parameter_form,
    }
    print(lighting_output_form)
    return render(request, 'main_scenario.html', context)
