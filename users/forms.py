from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile, UserToCompanyMapping


class AddInternalUserForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AddInternalUserForm2(forms.ModelForm):
    class Meta:
        model = UserToCompanyMapping
        fields = ['access_type']


class UpdateInUserForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active']

    # To disable the form fields in template(django won't look for it to update)
    def __init__(self, *args, **kwargs):
        super(UpdateInUserForm1, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True


# class UpdateInUserForm2(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['phone']
        # widgets = {
        #     'agreement_date': forms.TextInput(
        #         attrs={
        #             'type': 'date',
        #             'class': "form-control",
        #             'id': 'id_agreement_date'
        #         }),
        # }
