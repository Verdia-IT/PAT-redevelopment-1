from django import forms
from .models import LightingHourDetail, TIMES_CHOICES, LightingInput, LightingOutput
from references.models import LedLight, ExistingLight
from django.forms import ModelChoiceField



class LightingHourDetailForm(forms.ModelForm):

    class Meta:
        model = LightingHourDetail
        exclude = ['scenario']
        widgets = {
            'lighting_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_lighting_type',
                }),
            'monday_lighting_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_monday_lighting_hour_1_start',
                }),
            'monday_lighting_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_monday_lighting_hour_1_end',
                }),
            'monday_lighting_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_monday_lighting_hour_2_start',
                }),
            'monday_lighting_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_monday_lighting_hour_2_end',
                }),
            'tuesday_lighting_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_tuesday_lighting_hour_1_start',
                }),
            'tuesday_lighting_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_tuesday_lighting_hour_1_end',
                }),
            'tuesday_lighting_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_tuesday_lighting_hour_2_start',
                }),
            'tuesday_lighting_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_tuesday_lighting_hour_2_end',
                }),
            'wednesday_lighting_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_wednesday_lighting_hour_1_start',
                }),
            'wednesday_lighting_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_wednesday_lighting_hour_1_end',
                }),
            'wednesday_lighting_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_wednesday_lighting_hour_2_start',
                }),
            'wednesday_lighting_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_wednesday_lighting_hour_2_end',
                }),
            'thursday_lighting_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_thursday_lighting_hour_1_start',
                }),
            'thursday_lighting_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_thursday_lighting_hour_1_end',
                }),
            'thursday_lighting_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_thursday_lighting_hour_2_start',
                }),
            'thursday_lighting_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_thursday_lighting_hour_2_end',
                }),
            'friday_lighting_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_friday_lighting_hour_1_start',
                }),
            'friday_lighting_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_friday_lighting_hour_1_end',
                }),
            'friday_lighting_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_friday_lighting_hour_2_start',
                }),
            'friday_lighting_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_friday_lighting_hour_2_end',
                }),
            'saturday_lighting_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_saturday_lighting_hour_1_start',
                }),
            'saturday_lighting_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_saturday_lighting_hour_1_end',
                }),
            'saturday_lighting_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_saturday_lighting_hour_2_start',
                }),
            'saturday_lighting_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_saturday_lighting_hour_2_end',
                }),
            'sunday_lighting_hour_1_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_sunday_lighting_hour_1_start',
                }),
            'sunday_lighting_hour_1_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_sunday_lighting_hour_1_end',
                }),
            'sunday_lighting_hour_2_start': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_sunday_lighting_hour_2_start',
                }),
            'sunday_lighting_hour_2_end': forms.Select(
                choices=TIMES_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_hour_detail_sunday_lighting_hour_2_end',
                }),
        }
           

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.lighting_type

class LightingInputForm(forms.ModelForm):

    lighting_type = MyModelChoiceField(queryset=LightingHourDetail.objects.all(), widget=forms.Select(attrs={'class':'form-control','id':'lighting_input_lighting_type'}))
    existing_luminaire = forms.ModelChoiceField(queryset=ExistingLight.objects.all(), widget=forms.Select(attrs={'class':'form-control','id':'lighting_input_existing_luminaire'}))
    replacement_luminaire =  forms.ModelChoiceField(queryset=LedLight.objects.all(), widget=forms.Select(attrs={'class':'form-control','id':'lighting_input_replacement_luminaire'}))

    class Meta:
        model = LightingInput
        exclude = ['scenario']
        widgets = {
            'area': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_area',                    
                }),
            # 'lighting_type': forms.Select(                
            #     attrs={
            #         'class': 'form-control',
            #         'id': 'lighting_input_lighting_type',
            #     }),
            'number_of_existing_luminaire': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_number_of_existing_luminaire',
                }),
            # 'existing_luminaire': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #         'id': 'lighting_input_existing_luminaire',
            #     }),
            'existing_luminaire_power': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_existing_luminaire_power',
                }),
            'number_of_replaced_luminaire': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_number_of_replaced_luminaire',
                }),
            # 'replacement_luminaire': forms.Select(
            #     attrs={
            #         'class': 'form-control',
            #         'id': 'lighting_input_replacement_luminaire',
            #     }),
            'replacement_luminaire_power': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_replacement_luminaire_power',
                }),
            'power_reduction': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_power_reduction',
                    'readonly':'readonly',
                }),
            'estimated_operating_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_estimated_operating_hours',
                    'readonly':'readonly',
                }),
            'total_estimated_savings_kwhs': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_input_total_estimated_savings_kwhs',
                    'readonly':'readonly',
                }),
            'veec_discount': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_veec_discount',
                'readonly':'readonly',
            }),
            'esc_discount': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_esc_discount',
                'readonly':'readonly',
            }),
            'discount_adjustment': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_discount_adjustment',
            }),
            'total_discount': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_total_discount',
                'readonly':'readonly',
            }),
            'maintenance_savings': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_maintenance_savings',
            }),
            'dollar_per_fixture': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_dollar_per_fixture',
            }),
            'labour_per_hour': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_labour_per_hour',
            }),
            'fixtures_per_hour': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_fixtures_per_hour',
            }),
            'total_cost': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_total_cost',
                'readonly':'readonly',
            }),
            'led_life_in_months': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_led_life_in_months',
                'readonly':'readonly',
            }),
            'existing_lamp_replacement_costs': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_existing_lamp_replacement_costs',
                'readonly':'readonly',
            }),
            'existing_luminaire_life_in_months': forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'lighting_input_existing_luminaire_life_in_months',
                'readonly':'readonly',
            }), 
        
        }


class LightingOutputForm(forms.ModelForm):
    
    class Meta:
        model = LightingOutput
        exclude = ['scenario']
        widgets = {
            'number_of_lights': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_number_of_lights',  
                    'readonly':'readonly',                  
                }),
            'maintenance_savings': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_maintenance_savings', 
                    'readonly':'readonly',                   
                }),
            'power_reduction': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_power_reduction', 
                    'readonly':'readonly',                   
                }),
            'total_discount': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_total_discount', 
                    'readonly':'readonly',                   
                }),
            'installation_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_installation_cost',  
                    'readonly':'readonly',                  
                }),
            'other_adjustments_1': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_other_adjustments_1',                    
                }),
            'verdia_fee': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_verdia_fee',                    
                }),
            'verdia_fee_dollars': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_verdia_fee_dollars', 
                    'readonly':'readonly',                   
                }),
            'other_adjustments_2': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_other_adjustments_2',                    
                }),
            'total_cost': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'lighting_outputs_total_cost',
                    'readonly':'readonly',                    
                }),
        }




    
    