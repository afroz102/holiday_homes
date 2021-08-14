from django import forms
from units.models import Unit
from bookings.models import Booking, Guest


class AddBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['company', 'date_created',
                   'is_deleted', 'date_updated', 'added_by']

        widgets = {
            'unit': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'booking_source': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'address': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'city': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'country': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'booking_status': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'no_of_guest': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            # format = ('%d-%m-%Y'),  # default value is same
            'checkin_date': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'checkin_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'checkout_date': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'checkout_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

    # only Unit associated with company will be shown

    def __init__(self, company=None, *args, ** kwargs):
        super(AddBookingForm, self).__init__(*args, **kwargs)
        if company:
            self.fields['unit'].queryset = Unit.objects.filter(
                company=company, is_deleted=False)


class AddGuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'
        exclude = ['booking', 'date_created', 'is_deleted',
                   'date_updated', 'added_by']
        widgets = {
            'name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'email': forms.TextInput(attrs={
                'type': 'email',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'age': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'gender': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'document_type': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }


class UpdateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['company', 'added_by',
                   'date_created', 'date_updated', 'is_deleted']
        widgets = {
            'unit': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'booking_source': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'address': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'city': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'country': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'booking_status': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'no_of_guest': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            # format = ('%d-%m-%Y'),  # default value is same
            'checkin_date': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'checkin_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'checkout_date': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'checkout_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

    # only Landlord associated with company will be shown
    def __init__(self, *args, ** kwargs):
        super(UpdateBookingForm, self).__init__(*args, **kwargs)
        self.fields['unit'].disabled = True
        self.fields['booking_status'].disabled = True
