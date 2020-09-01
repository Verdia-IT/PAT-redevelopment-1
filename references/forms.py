from django import forms
from .models import PFCCost, SolarCost, SolarData


class PFCCostForm(forms.ModelForm):

    class Meta:
        model = PFCCost
        fields = ('pfc_rating', 'pfc_dollar_per_kvar')
        labels = {
            'pfc_rating': 'PFC Rating',
            'pfc_dollar_per_kvar': 'PFC ($/kvar)',
        }
        widgets = {
            'pfc_rating': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_cost_pfc_rating',
                }),
            'pfc_dollar_per_kvar': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'pfc_cost_pfc_dollar_per_kvar',
                }),
        }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        error_messages = {
            'pfc_rating': {
                'invalid': "PFC Rating can only take Integer fields",
            },
        }


class SolarCostForm(forms.ModelForm):

    class Meta:
        model = SolarCost
        fields = '__all__'
        widgets = {
            'system_size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_cost_system_size',
                }),
            'single_site_dollar_per_watt': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_cost_single_site_dollar_per_watt',
                }),
            'single_site_verdia_fee': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_cost_single_site_verdia_fee',
                }),
            'multi_site_dollar_per_watt': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_cost_multi_site_dollar_per_watt',
                }),
            'multi_site_verdia_fee': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_cost_multi_site_verdia_fee',
                }),
        }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'pfc_rating': {
        #         'invalid': "PFC Rating can only take Integer fields",
        #     },
        # }


# class SolarCostForm(forms.Form):
#     system_size = forms.IntegerField(widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':100,
#         }
#     ))
#     single_site_dollar_per_watt = forms.DecimalField(
#         max_digits=5, decimal_places=3,widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':100,
#         }
#     ))
#     single_site_verdia_fee = forms.DecimalField(
#         max_digits=5, decimal_places=3,widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':100,
#         }
#     ))
#     multiple_site_dollar_per_watt = forms.DecimalField(
#         max_digits=5, decimal_places=3,widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':100,
#         }
#     ))
#     multiple_site_verdia_fee = forms.DecimalField(
#         max_digits=5, decimal_places=3,widget=forms.TextInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':100,
#         }
#     ))



class SolarDataForm(forms.ModelForm):

    class Meta:
        model = SolarData
        fields = '__all__'

        widgets = {
            'file_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'solar_data_form_file_name',
                }),
            'solar_data_file': forms.FileInput(
                attrs={
                    'class': 'file1',
                    'id': 'solar_data_form_solar_data_file',
                }),
             
        }
