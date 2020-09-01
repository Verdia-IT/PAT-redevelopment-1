from django import forms
from .models import SolarLayout, SolarPrice, YES_NO_CHOICES, SYSTEM_TYPE_OVERRIDE_CHOICES, PFCPrice

class SolarLayoutForm(forms.ModelForm):

    class Meta:
        model = SolarLayout
        exclude = ['scenario','file_name']

        widgets = {
            
            'solar_layout_file': forms.FileInput(
                attrs={
                    'class': 'file1',
                    'id': 'solar_layout_form_solar_layout_file',
                }),  
        }

class SolarPriceForm(forms.ModelForm):
    
    class Meta:
        model = SolarPrice
        exclude = ['scenario']
        widgets = {
            'solar_size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_solar_size',  
                    'readonly':'readonly',                  
                }),
            'solar_unit_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_solar_unit_cost',  
                    'readonly':'readonly',                  
                }),
            'solar_unit_cost_override': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_solar_unit_cost_override',                                      
                }),
            'gross_system_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_gross_system_cost',  
                    'readonly':'readonly',                  
                }),
            'other_adjustments_1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_other_adjustments_1',                                      
                }),
            'verdia_fee': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_verdia_fee',                                      
                }),
            'verdia_fee_dollars': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_verdia_fee_dollars',  
                    'readonly':'readonly',                  
                }),
            'other_adjustments_2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_other_adjustments_2',                                      
                }),    
            'system_type': forms.TextInput(                
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_system_type',
                    'readonly':'readonly', 

                }),
            'system_type_override': forms.Select(
                choices=SYSTEM_TYPE_OVERRIDE_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_system_type_override',
                }),
            'stc_deeming_period': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_stc_deeming_period',                                      
                }),
            'stc_discount': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_stc_discount',  
                    'readonly':'readonly',                  
                }),
            'system_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_system_cost',  
                    'readonly':'readonly',                  
                }),
            'system_unit_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_system_unit_cost',  
                    'readonly':'readonly',                  
                }),
            'maintenance_cost_per_annum': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_maintenance_cost_per_annum',  
                    'readonly':'readonly',                  
                }),
            'include_solar_maintenance': forms.Select(
                choices=YES_NO_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'solar_price_include_solar_maintenance',
                }),
        }


    
class PFCPriceForm(forms.ModelForm):
    
    class Meta:
        model = PFCPrice
        exclude = ['scenario']
        widgets = {
            'pfc_size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_pfc_size',  
                    'readonly':'readonly',                  
                }),
            'pfc_unit_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_pfc_unit_cost',  
                    'readonly':'readonly',                  
                }),
            'pfc_unit_cost_override': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_pfc_unit_cost_override',                                     
                }),
            'gross_system_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_gross_system_cost',  
                    'readonly':'readonly',                  
                }),
            'verdia_fee': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_verdia_fee',                                      
                }),
            'verdia_fee_dollars': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_verdia_fee_dollars',  
                    'readonly':'readonly',                  
                }),
            'system_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_system_cost',  
                    'readonly':'readonly',                  
                }),
            'system_unit_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_price_system_unit_cost',  
                    'readonly':'readonly',                  
                }),
        }