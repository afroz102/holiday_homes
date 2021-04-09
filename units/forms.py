from django import forms
from units.models import Unit
from landlords.models import Landlord


class AddUnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'
        exclude = ['company', 'date_created',
                   'date_updated', 'added_by']

    # only Landlord associated with company will be shown
    def __init__(self, managed_by=None, *args, ** kwargs):
        super(AddUnitForm, self).__init__(*args, **kwargs)
        if managed_by:
            self.fields['landlord'].queryset = Landlord.objects.filter(
                managed_by=managed_by, is_deleted=False)


class UpdateUnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'
        exclude = ['company', 'date_created',
                   'date_updated', 'added_by']

    # only Landlord associated with company will be shown
    def __init__(self, *args, ** kwargs):
        super(UpdateUnitForm, self).__init__(*args, **kwargs)
        self.fields['landlord'].disabled = True
