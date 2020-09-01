from django import forms
from .models import (Scenario, IntervalData)



class ScenarioForm(forms.ModelForm):    

    class Meta:
        model = Scenario
        exclude = ['site_name','program_name']
        widgets = {
            'scenario_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'scenario_details_scenario_name',
                }),
            'notes': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'scenario_details_notes',
                }),  

        }


class IntervalDataForm(forms.ModelForm):

    class Meta:
        model = IntervalData
        exclude = ['scenario','file_name']

        widgets = {
            
            'interval_data_file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'interval_data_form_interval_data_file',
                }),  
        }
