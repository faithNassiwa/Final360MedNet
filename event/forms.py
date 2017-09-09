from django import forms


class EventSearchForm(forms.Form):
    search_field = forms.CharField(max_length=100, required=True)
    events_region = forms.CharField(max_length=100)
    events_date = forms.CharField(max_length=100)