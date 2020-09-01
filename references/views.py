from django.shortcuts import render, get_object_or_404
from .models import CertificatePrices, TariffEscalations, PeakEnergyRates, OffpeakEnergyRates, SolarCost, SolarData
from .forms import PFCCostForm, SolarCostForm, SolarDataForm
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/")
def references_page(request):
    certificate_data = get_object_or_404(CertificatePrices, id=1)
    tariff_escalations_2019 = get_object_or_404(TariffEscalations, year=2019)
    tariff_escalations_2020 = get_object_or_404(TariffEscalations, year=2020)
    tariff_escalations_2021 = get_object_or_404(TariffEscalations, year=2021)
    tariff_escalations_2022 = get_object_or_404(TariffEscalations, year=2022)
    tariff_escalations_2023 = get_object_or_404(TariffEscalations, year=2023)
    tariff_escalations_2024 = get_object_or_404(TariffEscalations, year=2024)
    tariff_escalations_2025 = get_object_or_404(TariffEscalations, year=2025)
    tariff_escalations_2026 = get_object_or_404(TariffEscalations, year=2026)
    tariff_escalations_2027 = get_object_or_404(TariffEscalations, year=2027)
    peak_energy_rates_2020 = get_object_or_404(PeakEnergyRates, year=2020)
    peak_energy_rates_2021 = get_object_or_404(PeakEnergyRates, year=2021)
    peak_energy_rates_2022 = get_object_or_404(PeakEnergyRates, year=2022)
    offpeak_energy_rates_2020 = get_object_or_404(OffpeakEnergyRates, year=2020)
    offpeak_energy_rates_2021 = get_object_or_404(OffpeakEnergyRates, year=2021)
    offpeak_energy_rates_2022 = get_object_or_404(OffpeakEnergyRates, year=2022)
    solar_cost = SolarCost.objects.order_by('system_size')
    pfc_cost_form = PFCCostForm()
    solar_cost_form = SolarCostForm()
    solar_data_form = SolarDataForm()
    
    context = {
        'certificate_data': certificate_data,
        'tariff_escalations_2019': tariff_escalations_2019,
        'tariff_escalations_2020': tariff_escalations_2020,
        'tariff_escalations_2021': tariff_escalations_2021,
        'tariff_escalations_2022': tariff_escalations_2022,
        'tariff_escalations_2023': tariff_escalations_2023,
        'tariff_escalations_2024': tariff_escalations_2024,
        'tariff_escalations_2025': tariff_escalations_2025,
        'tariff_escalations_2026': tariff_escalations_2026,
        'tariff_escalations_2027': tariff_escalations_2027,
        'peak_energy_rates_2020': peak_energy_rates_2020,
        'peak_energy_rates_2021': peak_energy_rates_2021,
        'peak_energy_rates_2022': peak_energy_rates_2022,
        'offpeak_energy_rates_2020': offpeak_energy_rates_2020,
        'offpeak_energy_rates_2021': offpeak_energy_rates_2021,
        'offpeak_energy_rates_2022': offpeak_energy_rates_2022,
        'solar_cost': solar_cost,
        'pfc_cost_form': pfc_cost_form,
        'solar_cost_form': solar_cost_form,
        'solar_data_form' : solar_data_form,
    }
    return render(request, 'references.html', context)



