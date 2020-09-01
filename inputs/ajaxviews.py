from django.shortcuts import render, get_object_or_404
from scenarios.models import Scenario

from .models import (BillDetail, OperatingHourDetail, HolidayDetail,
                     PriceForecastOverride, EscalationsOverride, SolarExport)
from .forms import (BillDetailForm, OperatingHourDetailForm, HolidayDetailForm,
                    PriceForecastOverrideForm, EscalationsOverrideForm, SolarExportForm)

from django.http import JsonResponse, HttpResponse
import json


# --------------------------General helper functions for views -------------------


# ------------------------------- Ajax Views ---------------------------------------

def save_bill_detail_page(request):
    data = {}
    if request.is_ajax():
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        bill_detail = BillDetail.objects.all().filter(scenario=scenario).first()
        form = BillDetailForm(request.POST, instance=bill_detail)

        if form.is_valid():
            try:
                bill_detail = form.save(commit=False)
                bill_detail.scenario = scenario
                bill_detail.save()
                data['message'] = 'Success'
            except Exception as e:
                data['message'] = str(e)
        else:
            data['message'] = form.errors
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def save_operating_hour_detail_page(request):
    data = {}
    if request.is_ajax():
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        operating_hour_detail = OperatingHourDetail.objects.all().filter(
            scenario=scenario).first()
        form = OperatingHourDetailForm(
            request.POST, instance=operating_hour_detail)

        if form.is_valid():
            try:
                operating_hour_detail = form.save(commit=False)
                operating_hour_detail.scenario = scenario
                operating_hour_detail.save()
                data['message'] = 'Success'
            except Exception as e:
                data['message'] = str(e)
        else:
            data['message'] = form.errors
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def save_holiday_detail_page(request):
    data = {}
    if request.is_ajax():
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        holiday_detail = HolidayDetail.objects.all().filter(scenario=scenario).first()
        form = HolidayDetailForm(request.POST, instance=holiday_detail)

        if form.is_valid():
            try:
                holiday_detail = form.save(commit=False)
                holiday_detail.scenario = scenario
                holiday_detail.save()
                data['message'] = 'Success'
            except Exception as e:
                data['message'] = str(e)
        else:
            data['message'] = form.errors
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def save_price_forecast_override_page(request):
    data = {}
    if request.is_ajax():
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        price_forecast_override = PriceForecastOverride.objects.all().filter(
            scenario=scenario).first()
        form = PriceForecastOverrideForm(
            request.POST, instance=price_forecast_override)

        if form.is_valid():
            try:
                price_forecast_override = form.save(commit=False)
                price_forecast_override.scenario = scenario
                price_forecast_override.save()
                data['message'] = 'Success'
            except Exception as e:
                data['message'] = str(e)
        else:
            data['message'] = form.errors
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def save_escalations_override_page(request):
    data = {}
    if request.is_ajax():
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        escalations_override = EscalationsOverride.objects.all().filter(
            scenario=scenario).first()
        form = EscalationsOverrideForm(
            request.POST, instance=escalations_override)

        if form.is_valid():
            try:
                escalations_override = form.save(commit=False)
                escalations_override.scenario = scenario
                escalations_override.save()
                data['message'] = 'Success'
            except Exception as e:
                data['message'] = str(e)
        else:
            data['message'] = form.errors
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))


def save_solar_export_page(request):
    data = {}
    if request.is_ajax():
        scenario_id = request.POST['scenarioId']
        scenario = get_object_or_404(Scenario, id=scenario_id)
        solar_export = SolarExport.objects.all().filter(scenario=scenario).first()
        form = SolarExportForm(
            request.POST, instance=solar_export)

        if form.is_valid():
            try:
                solar_export = form.save(commit=False)
                solar_export.scenario = scenario
                solar_export.save()
                data['message'] = 'Success'
            except Exception as e:
                data['message'] = str(e)
        else:
            data['message'] = form.errors
    else:
        data['message'] = 'Not Ajax'
    return HttpResponse(json.dumps(data))
