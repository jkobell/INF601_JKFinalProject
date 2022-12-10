# INF601 - Advanced Programming in Python
# James Kobell
# Final Project
import dateparser as dp # for parse json datetime string value
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.cache import never_cache
from .models import Ticker
from .forms import EodForm, DateForm, EodCheckboxForm, ChartMovingAverageRadio
from .fin_api import FinApi
from .moving_avg import MovingAvg
import json

@never_cache
def register(request): # user register form
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # username, password1, password2
        if form.is_valid():
            form.save()
            messages.success(request, f'Registration successful. Please log in.')    
            return redirect('login_request')
        #else: 
           # messages.error(request, f'is form valid: {form.is_valid()}') #uncomment to debug if form is valid 
    else:
        if request.user.is_authenticated:
            logout(request)
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'charts/register.html', context)

@never_cache
def login_request(request): #login form
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST) # username, password
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"You are now logged in as {username}.") #uncomment to debug
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'charts/login.html', context)

@never_cache
def logout_request(request):     
    logout(request) #flushes Session
    #messages.info(request, f"You are now logged out.") #uncomment to debug
    return redirect('index')

@never_cache
def renderDashboard(request, chart_img): # clears all forms, passes chart img as param
        form = EodForm()
        date_form = DateForm()
        checkbox_form = EodCheckboxForm()
        conf_chart_radio_form = ChartMovingAverageRadio()
        context = { #params: page name, list of links
            'page_name': 'Dashboard',
            'form': form,
            'date_form': date_form,
            'checkbox_form': checkbox_form,
            'conf_chart_radio_form': conf_chart_radio_form,
            'chart_img': chart_img,
        }    
        return render(request, 'charts/index.html', context=context)

#index user dashboard view with forms
@never_cache
def index(request):
    messages.get_messages(request).used = True
    if request.method == 'POST':
        form = EodForm(data=request.POST)
        date_form = DateForm(data=request.POST)
        checkbox_form = EodCheckboxForm(data=request.POST)
        conf_chart_radio_form = ChartMovingAverageRadio(data=request.POST)

        if form.is_valid() and conf_chart_radio_form.is_valid():
            img_chart = getApiEodLimit(conf_chart_radio_form.cleaned_data['mov_av_radio'] , form.cleaned_data['ticker_choice'])
            return renderDashboard(request, img_chart)

        elif form.is_valid() and date_form.is_valid() and checkbox_form.is_valid():
            eod_data = getApiEod(date_form.cleaned_data['date_field'] , form.cleaned_data['ticker_choice'], checkbox_form.data.get('is_latest'))            
            pagination_count = eod_data['pagination']['count']
            if pagination_count > 0:
                data = eod_data['data'] #get data object from json                
                time = dp.parse(data[0]['date']) # convert value to datetime object
                ftime = time.strftime("%m/%d/%Y") # format date - 01/01/2099
                context = {
                    'eod_data': data, 
                    'eod_date': ftime, 
                    'page_name': 'End of Day'
                    }
            else:
                context = {
                    'error_data_message': 'No EOD data is available for the selected date.',
                    }
            return render(request, 'charts/eod_data.html', context) 
        else:
            messages.error(request,"Error on submit.")            
    
    param = None
    return renderDashboard(request, param)
    
def getApiEod(eod_date, ticker, is_latest):
    fin_api = FinApi()

    try:
        query_results = Ticker.objects.get(name=ticker)
    except Ticker.DoesNotExist:
        raise Http404() # todo - logging please
    
    symbol = query_results.symbol
    return fin_api.getEod(eod_date, symbol, is_latest)

def getApiEodLimit(limit, ticker):
    fin_api = FinApi()
    mov_avg = MovingAvg()
    match limit:
        case '1':
            eod_limit = '50'
        case '2':
            eod_limit = '100'
        case '3':
            eod_limit = '200'
        case '4':
            eod_limit = '400'
        case _:
            raise ValueError("Not a valid limit.")

    try:
        query_results = Ticker.objects.get(name=ticker)
    except Ticker.DoesNotExist:
        raise Http404() #logging please
    
    symbol = query_results.symbol
    #print(f'SYMBOL: {symbol}') #for debug purposes
    #print(f'LIMIT: {eod_limit}')#for debug purposes
    
    raw = fin_api.getEodLimit(eod_limit, symbol)
    raw_data = raw['data']
    str_data = json.dumps(raw_data)
        
    svg_chart = mov_avg.BuildMovAvgChart(str_data, eod_limit)
    return svg_chart
