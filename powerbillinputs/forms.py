from django import forms
from .models import (EnergyCharge, DemandCharge, FixedCharge,
                     TIMES_CHOICES, ENERGY_TARIFF_TYPE_CHOICES, CATEGORY_CHOICES, YES_NO_CHOICES,
                     DEMAND_TARIFF_TYPE_CHOICES, CHARGEABLE_POWER_TYPE_CHOICES,
                     FREQUENCY_CHOICES)
from scenarios.models import Scenario


class EnergyChargeForm(forms.ModelForm):

    # def clean_amount(self):
    #     amount = self.cleaned_data.get('amount')
    #     if amount > 0.5:
    #         raise forms.ValidationError('Amount cannot be greater than $0.5')
    #     return amount

    # if validation takes more than 1 field, use clean only method as below
    # def clean(self):
    #     cleaned_data = super().clean()
    #     amount = cleaned_data.get('amount')

    #     if amount>0.5:
    #         raise forms.ValidationError('Amount cannot be greaters than $0.5')

    class Meta:
        model = EnergyCharge
        exclude = ['scenario']
        widgets = {
            'tariff_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_tariff_name',
                }),
            'include': forms.Select(
                choices=YES_NO_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_include',
                }),
            'amount': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_amount',
                }),
            'tariff_type': forms.Select(
                choices=ENERGY_TARIFF_TYPE_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_tariff_type',
                }),
            'weekday_start_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_weekday_start_time',
                }),
            'weekday_end_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_weekday_end_time',
                }),
            'weekend_start_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_weekend_start_time',
                }),
            'weekend_end_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_weekend_end_time',
                }),
            'months': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_months',
                }),
            'category': forms.Select(
                choices=CATEGORY_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'energy_charge_category',
                }),


        }


class DemandChargeForm(forms.ModelForm):

    class Meta:
        model = DemandCharge
        exclude = ['scenario']
        widgets = {
            'tariff_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_tariff_name',
                }),
            'include': forms.Select(
                choices=YES_NO_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_include',
                }),
            'chargeable_power': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_chargeable_power',
                }),
            'amount': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_amount',
                }),
            'tariff_type': forms.Select(
                choices=DEMAND_TARIFF_TYPE_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_tariff_type',
                }),
            'weekday_start_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_weekday_start_time',
                }),
            'weekday_end_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_weekday_end_time',
                }),
            'weekend_start_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_weekend_start_time',
                }),
            'weekend_end_time': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_weekend_end_time',
                }),
            'chargeable_power_type': forms.Select(
                choices=CHARGEABLE_POWER_TYPE_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_chargeable_power_type',
                }),            
            'months': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_months',
                }),
            'threshold': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_threshold',
                }),
            'category': forms.Select(
                choices=CATEGORY_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'demand_charge_category',
                }),
        }


class FixedChargeForm(forms.ModelForm):

    class Meta:
        model = FixedCharge
        exclude = ['scenario']
        widgets = {
            'tariff_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'fixed_charge_tariff_name',
                }),
            'include': forms.Select(
                choices=YES_NO_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'fixed_charge_include',
                }),            
            'amount': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'fixed_charge_amount',
                }),
            'frequency': forms.Select(
                choices=FREQUENCY_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'fixed_charge_frequency',
                }),         
            'category': forms.Select(
                choices=CATEGORY_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'fixed_charge_category',
                }),
        }