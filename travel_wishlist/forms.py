from django import forms
from .models import Place 

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place 
        fields = ('name', 'visited')

class DateInput(forms.DateInput):
    input_type = 'date'  # Override the default input type, which is 'text'. 


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }
