from django import forms
from django.contrib.admin import widgets
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware
from django.forms import TextInput, MultiWidget, DateTimeField


# nightmare discussion here https://stackoverflow.com/questions/38601/using-django-time-date-widgets-in-custom-form
class MinimalSplitDateTimeMultiWidget(MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        if widgets is None:
            if attrs is None:
                attrs = {}
            date_attrs = attrs.copy()
            time_attrs = attrs.copy()

            date_attrs['type'] = 'date'
            time_attrs['type'] = 'time'

            widgets = [
                TextInput(attrs=date_attrs),
                TextInput(attrs=time_attrs),
            ]
        super().__init__(widgets, attrs)

    # nabbing from https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#django.forms.MultiWidget.decompress
    def decompress(self, value):
        if value:
            return [value.date(), value.strftime('%H:%M')]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_str, time_str = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.

        if date_str == time_str == '':
            return None

        if time_str == '':
            time_str = '00:00'

        my_datetime = datetime.strptime(date_str + time_str, "%Y-%m-%d%H:%M")

        # making timezone aware
        return make_aware(my_datetime)

class EventForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Description'}))
    start_datetime = forms.DateTimeField()
    end_datetime = forms.DateTimeField()
    inventory_tier = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Inventory Tier'}))
    ticket_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder': 'Ticket Price'}))
    ticket_capacity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ticket Capacity'}))
    venue_name = forms.CharField(max_length=244,
                                 widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Venue Name'}))
    latitude = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Latitude'}))
    longitude = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Longitude'}))

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_datetime'].widget = MinimalSplitDateTimeMultiWidget()
        self.fields['end_datetime'].widget = MinimalSplitDateTimeMultiWidget()

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_datetime')
        end_date = cleaned_data.get('end_datetime')

        # Check if start date is not less than today
        if start_date and start_date < timezone.now():
            raise forms.ValidationError("Start date cannot be in the past.")

        # Check if end date is not less than start date
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be less than start date.")

        return cleaned_data