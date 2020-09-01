from django import forms
from .models import SimulationParameter, YES_NO_CHOICES
from scenarios.models import IntervalData
from django.forms import ModelChoiceField


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.file_name

class SimulationParameterForm(forms.ModelForm):

    interval_data = ModelChoiceField(queryset=IntervalData.objects.all(), widget=forms.Select(attrs={'class':'form-control','id':'simulation_parameter_interval_data'}))
    # existing_luminaire = forms.ModelChoiceField(queryset=ExistingLight.objects.all(), widget=forms.Select(attrs={'class':'form-control','id':'lighting_input_existing_luminaire'}))
    # replacement_luminaire =  forms.ModelChoiceField(queryset=LedLight.objects.all(), widget=forms.Select(attrs={'class':'form-control','id':'lighting_input_replacement_luminaire'}))

    class Meta:
        model = SimulationParameter
        exclude = ['scenario']
        widgets = {            
            'include_lighting': forms.Select(
                choices=YES_NO_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'simulation_parameter_include_lighting',
                }),
            'solar_size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'simulation_parameter_solar_size',                    
                }),
            'pfc_size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'simulation_parameter_pfc_size',                    
                }),
            'target_pf': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'simulation_parameter_target_pf',                    
                }),
        }


