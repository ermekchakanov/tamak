from django import forms
from .models import Order

class ReservationForm(forms.ModelForm):
    '''Форма создвания Брони. Унаследована у модели Orders.'''
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['reservator', 'date_created']
   
