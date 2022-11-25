
import datetime
from django import forms
from .models import Ticker

YEAR_CHOICES = ['2015','2016','2017','2018','2019','2020','2021','2022', '2023','2024','2025','2026','2027','2028',]

class EodForm(forms.Form):
    query = Ticker.objects.all().distinct().order_by('name')
    #query_choices = [(ticker.name, f"{ticker.name} - {ticker.symbol}") for ticker in query] #default=0
    query_choices = [('', 'Select ticker')] + [(ticker.name, f"{ticker.name} - {ticker.symbol}") for ticker in query]
    ticker_choices = forms.ChoiceField(choices=query_choices, required=False, widget=forms.Select(attrs={'style': 'width:100%; text-align:center;'}), label='Tickers')

class DateForm(forms.Form):
        #date_field = forms.DateField(required=True, label='EOD Date', initial = datetime.date.today()).widget_attrs() #enter date into field box
        date_field = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES, 
                                     attrs={'style': 'width:100%; text-align:center'}), label='EOD Date')
        
    