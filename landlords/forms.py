from django import forms
from users.models import UserProfile
from landlords.models import Landlord, LandlordDocument


class AddLandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = '__all__'
        exclude = ['managed_by', 'date_created',
                   'date_updated', 'added_by', 'status']

        widgets = {
            'agreement_date': forms.TextInput(
                attrs={
                    'type': 'date',
                    'class': "form-control",
                    'id': 'id_agreement_date'
                }),
        }

    # only User associated with agency will be shown
    # def __init__(self, agency=None, *args, ** kwargs):
    #     super(CreateClientForm, self).__init__(*args, **kwargs)
    #     if agency:
    #         self.fields['client_account_manager'].queryset = UserProfile.objects.filter(
    #             agency=agency, is_deleted=False)


class AddLandlordDocForm(forms.ModelForm):
    class Meta:
        model = LandlordDocument
        fields = ['doc_name', 'doc_file', 'expiry_date']

        widgets = {
            'doc_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'id': 'id_doc_name'
            }),
            'doc_file': forms.FileInput(attrs={
                'type': 'file',
                'class': "form-control",
                'id': 'id_doc_file'
            }),
            'expiry_date': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'id': 'id_expiry_date'
            }),
        }
