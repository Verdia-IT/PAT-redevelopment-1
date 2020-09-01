from django import forms
from .models import (Site, STATE_CHOICES, INDUSTRY_TYPE_CHOICES,
                     SOLAR_DATA_CHOICES, DNSP_CHOICES)
from programs.models import Program


class SiteForm(forms.ModelForm):
    # program_name = forms.ModelChoiceField(queryset=Program.objects.all())

    class Meta:
        model = Site
        # fields = ['site_name','NMI','street_address','city','state','postcode','DNSP','industry_type','default_solar_data']
        exclude = ['program_name']
        widgets = {
            'site_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_site_name',
                }),
            'NMI': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_NMI',
                }),
            'street_address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_street_address',
                }),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_city',
                }),
            'state': forms.Select(
                choices= STATE_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_state',
                }),
            'postcode': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_postcode',
                }),
            'DNSP': forms.Select(
                choices= DNSP_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_DNSP',
                }),
            'industry_type': forms.Select(
                choices= INDUSTRY_TYPE_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_industry_type',
                }),
            'default_solar_data': forms.Select(
                choices= SOLAR_DATA_CHOICES,
                attrs={
                    'class': 'form-control',
                    'id': 'modal_new_site_default_solar_data',
                }),
            

        }
