from django import forms
from units.models import Unit
from bookings.models import Booking
from tasks.models import TaskManager, Task
from users.models import UserProfile


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['unit', 'booking', 'task_title', 'task_details',
                  'task_date', 'task_time', 'task_status']
        widgets = {
            'unit': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'booking': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'task_title': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'task_details': forms.Textarea(attrs={
                'type': 'text',
                'rows': '2',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),

            'task_status': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            # format = ('%d-%m-%Y'),  # default value is same
            'task_date': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'task_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

    # only Unit associated with company will be shown

    def __init__(self, company=None, unit=None, *args, ** kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        if company:
            self.fields['unit'].queryset = Unit.objects.filter(
                company=company, is_deleted=False)

            # Further filter booking field
            if unit:
                self.fields['booking'].queryset = Booking.objects.filter(
                    unit=unit)
            else:
                self.fields['booking'].queryset = Booking.objects.filter(
                    company=company)


class AddTaskManagerForm(forms.ModelForm):
    class Meta:
        model = TaskManager
        fields = ['assigned_to']

        widgets = {
            'assigned_to': forms.SelectMultiple(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            })
        }

    def __init__(self, company=None, *args, ** kwargs):
        super(AddTaskManagerForm, self).__init__(*args, **kwargs)
        if company:
            self.fields['assigned_to'].queryset = UserProfile.objects.filter(
                company=company)


class AddSingleTaskManagerForm(forms.ModelForm):
    class Meta:
        model = TaskManager
        fields = ['assigned_to']

        widgets = {
            'assigned_to': forms.Select(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            })
        }

    def __init__(self, company=None, *args, ** kwargs):
        super(AddSingleTaskManagerForm, self).__init__(*args, **kwargs)
        if company:
            self.fields['assigned_to'].queryset = UserProfile.objects.filter(
                company=company)


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['unit', 'booking', 'task_title', 'task_details',
                  'task_date', 'task_time', 'task_status']
        widgets = {
            'unit': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'booking': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'task_title': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'task_details': forms.Textarea(attrs={
                'type': 'text',
                'rows': '2',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),

            'task_status': forms.Select(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            # format = ('%d-%m-%Y'),  # default value is same
            'task_date': forms.DateInput(attrs={
                'type': 'date',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'task_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

    # disable some field for update

    def __init__(self, *args, ** kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        self.fields['unit'].disabled = True
        self.fields['booking'].disabled = True
        self.fields['task_status'].disabled = True


class UpdateTaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_status']

        widgets = {
            'task_status': forms.Select(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            })
        }
