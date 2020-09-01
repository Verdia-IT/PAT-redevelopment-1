from django import forms
from .models import Program, ProgramOverride, MONTH_2_CHOICES


class ProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = '__all__'        
        widgets = {
            'program_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_program_program_name',
                }),
            'salesforce_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_program_salesforce_id',
                }),
            'contact_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_program_contact_name',
                }),
            'contact_title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_program_contact_title',
                }),
            'contact_email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_program_contact_email',
                }),
            'contact_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_program_contact_phone',
                }),
            
        }
        
     
class ProgramOverrideForm(forms.ModelForm):

    class Meta:
        model = ProgramOverride
        exclude = ['program']
        widgets = {            
            'cashflow_start_month': forms.Select(
                choices=MONTH_2_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'cashflow_start_month',
                }),
            'cashflow_start_year': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'cashflow_start_year'
                }),
            'discount_rate': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'discount_rate'
                }),            
            
        }

    def clean_cashflow_start_year(self):
        cashflow_start_year = self.cleaned_data.get("cashflow_start_year")
        if cashflow_start_year < 2017 or cashflow_start_year > 2045:
            raise forms.ValidationError("Cashflow start year is not in suitable range")
        return cashflow_start_year