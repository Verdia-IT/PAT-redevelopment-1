from django import forms
from .models import (BillDetail, OperatingHourDetail, HolidayDetail, PriceForecastOverride, EscalationsOverride, SolarExport,
                     ELECTRICIY_RETAILER_CHOICES, MONTH_CHOICES, TIMES_CHOICES, MONTH_2_CHOICES, YES_NO_CHOICES)
from scenarios.models import Scenario


class BillDetailForm(forms.ModelForm):

    class Meta:
        model = BillDetail
        exclude = ['scenario']
        widgets = {
            'number_of_bills': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'bill_detail_number_of_bills',
                }),
            'bill_month': forms.Select(
                choices=MONTH_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'bill_detail_bill_month',
                }),
            'bill_year': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'bill_detail_bill_year',
                }),
            'bill_days': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'bill_detail_bill_days',
                }),
            'electricity_retailer': forms.Select(
                choices=ELECTRICIY_RETAILER_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'bill_detail_electricity_retailer',
                }),
            'kwhs_consumed': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'bill_detail_kwhs_consumed',
                }),

        }

class OperatingHourDetailForm(forms.ModelForm):

    class Meta:
        model = OperatingHourDetail
        exclude = ['scenario']
        widgets = {
            'monday_operating_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_monday_operating_hour_1_start',
                }),
            'monday_operating_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_monday_operating_hour_1_end',
                }),
            'monday_operating_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_monday_operating_hour_2_start',
                }),
            'monday_operating_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_monday_operating_hour_2_end',
                }),
            'tuesday_operating_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_tuesday_operating_hour_1_start',
                }),
            'tuesday_operating_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_tuesday_operating_hour_1_end',
                }),
            'tuesday_operating_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_tuesday_operating_hour_2_start',
                }),
            'tuesday_operating_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_tuesday_operating_hour_2_end',
                }),
            'wednesday_operating_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_wednesday_operating_hour_1_start',
                }),
            'wednesday_operating_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_wednesday_operating_hour_1_end',
                }),
            'wednesday_operating_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_wednesday_operating_hour_2_start',
                }),
            'wednesday_operating_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_wednesday_operating_hour_2_end',
                }),
            'thursday_operating_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_thursday_operating_hour_1_start',
                }),
            'thursday_operating_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_thursday_operating_hour_1_end',
                }),
            'thursday_operating_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_thursday_operating_hour_2_start',
                }),
            'thursday_operating_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_thursday_operating_hour_2_end',
                }),
            'friday_operating_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_friday_operating_hour_1_start',
                }),
            'friday_operating_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_friday_operating_hour_1_end',
                }),
            'friday_operating_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_friday_operating_hour_2_start',
                }),
            'friday_operating_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_friday_operating_hour_2_end',
                }),
            'saturday_operating_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_saturday_operating_hour_1_start',
                }),
            'saturday_operating_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_saturday_operating_hour_1_end',
                }),
            'saturday_operating_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_saturday_operating_hour_2_start',
                }),
            'saturday_operating_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_saturday_operating_hour_2_end',
                }),
            'sunday_operating_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_sunday_operating_hour_1_start',
                }),
            'sunday_operating_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_sunday_operating_hour_1_end',
                }),
            'sunday_operating_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_sunday_operating_hour_2_start',
                }),
            'sunday_operating_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'operating_hour_detail_sunday_operating_hour_2_end',
                }),

        }

class HolidayDetailForm(forms.ModelForm):

    class Meta:
        model = HolidayDetail
        exclude = ['scenario']
        widgets = {
            'holiday_period_1_start_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_1_start_date',
                }),
            'holiday_period_1_start_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_1_start_month',
                }),
            'holiday_period_1_end_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_1_end_date',
                }),
            'holiday_period_1_end_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_1_end_month',
                }),
            'holiday_period_2_start_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_2_start_date',
                }),
            'holiday_period_2_start_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_2_start_month',
                }),
            'holiday_period_2_end_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_2_end_date',
                }),
            'holiday_period_2_end_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_2_end_month',
                }),
            'holiday_period_3_start_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_3_start_date',
                }),
            'holiday_period_3_start_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_3_start_month',
                }),
            'holiday_period_3_end_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_3_end_date',
                }),
            'holiday_period_3_end_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_3_end_month',
                }),
            'holiday_period_4_start_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_4_start_date',
                }),
            'holiday_period_4_start_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_4_start_month',
                }),
            'holiday_period_4_end_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_4_end_date',
                }),
            'holiday_period_4_end_month': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'holiday_detail_holiday_period_4_end_month',
                }),         

        }


class PriceForecastOverrideForm(forms.ModelForm):

    class Meta:
        model = PriceForecastOverride
        exclude = ['scenario']
        widgets = {
            'year_2019': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2019',
                }),
             'year_2020': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2020',
                }),
             'year_2021': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2021',
                }),
             'year_2022': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2022',
                }),
             'year_2023': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2023',
                }),
             'year_2024': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2024',
                }),
             'year_2025': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2025',
                }),
             'year_2026': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2026',
                }),
             'year_2027': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'price_forecast_override_year_2027',
                }),
        }
   

class EscalationsOverrideForm(forms.ModelForm):

    class Meta:
        model = EscalationsOverride
        exclude = ['scenario']
        widgets = {
            'month_1': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_month_1',
                }),
            'year_1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_year_1',
                }),
            'override_1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_override_1',
                }),
            'month_2': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_month_2',
                }),
            'year_2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_year_2',
                }),
            'override_2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_override_2',
                }),
            'month_3': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_month_3',
                }),
            'year_3': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_year_3',
                }),
            'override_3': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_override_3',
                }),
            'month_4': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_month_4',
                }),
            'year_4': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_year_4',
                }),
            'override_4': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_override_4',
                }),
            'month_5': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_month_5',
                }),
            'year_5': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_year_5',
                }),
            'override_5': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_override_5',
                }),
            'month_6': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_month_6',
                }),
            'year_6': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_year_6',
                }),
            'override_6': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'escalations_override_override_6',
                }), 
        }  


class SolarExportForm(forms.ModelForm):

    class Meta:
        model = SolarExport
        exclude = ['scenario']
        widgets = {
            'include_solar_export': forms.Select(
                choices=YES_NO_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_include_solar_export',
                }),
            'year_2019': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2019',
                }),
            'year_2020': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2020',
                }),
            'year_2021': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2021',
                }),
            'year_2022': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2022',
                }),
            'year_2023': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2023',
                }),
            'year_2024': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2024',
                }),
            'year_2025': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2025',
                }),
            'year_2026': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2026',
                }),
            'year_2027': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2027',
                }),
            'year_2028': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2028',
                }),
            'year_2029': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2029',
                }),
            'year_2030': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2030',
                }),
            'year_2031': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_export_year_2031',
                }),
        }