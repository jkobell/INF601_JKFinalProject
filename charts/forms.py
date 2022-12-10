# INF601 - Advanced Programming in Python
# James Kobell
# Final Project
from django import forms
from .models import Ticker

YEAR_CHOICES = ['2015','2016','2017','2018','2019','2020','2021','2022', '2023','2024','2025','2026','2027','2028',]

class EodForm(forms.Form): #Tickers dropdown form
    query = Ticker.objects.all().distinct().order_by('name')
    query_choices = [('', 'Select ticker')] + [(ticker.name, f"{ticker.name} - {ticker.symbol}") for ticker in query]
    ticker_choice = forms.ChoiceField(choices=query_choices, required=True, widget=forms.Select(attrs={'style': 'width:100%; text-align:center;'}), label='Ticker')

class DateForm(forms.Form): #Date picker form
    date_field = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES, 
                                    attrs={'style': 'width:100%; text-align:center'}), label='EOD Date')

class EodCheckboxForm(forms.Form): # eod latest checkbox form
    is_latest = forms.BooleanField(label='Latest', required=False, initial=False)

class ChartMovingAverageRadio(forms.Form): # chart config date range radios form
    CHOICES = [('1', '50 Day'), ('2', '100 Day'), ('3', '200 Day'), ('4', '400 Day')]
    mov_av_radio = forms.ChoiceField(widget=forms.RadioSelect, required=True, label='Moving Average', initial=1, choices=CHOICES)

    
        
    