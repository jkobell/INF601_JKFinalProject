# INF601 - Advanced Programming in Python
# James Kobell
# Final Project
import dateparser as dp # for parse json datetime string value
#from django.utils import formats
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.cache import never_cache
from .models import Exchange, Currency, Ticker
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
def renderDashboard(request, chart_img):
        form = EodForm()
        date_form = DateForm()
        checkbox_form = EodCheckboxForm()
        conf_chart_radio_form = ChartMovingAverageRadio()
        pages_list = ['exchange', 'currency', 'ticker'] #todo - move to model
        context = { #params: page name, list of links
            'page_name': 'Dashboard',
            'pages_list': pages_list,
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
            #print('test limit call')
            #print(img_chart)
            #request = None
            print('im in conf chart if')
            #return renderDashboard(request, img_chart)
            return renderDashboard(request, img_chart)
            #return HttpResponseRedirect(reverse('index'))

        elif form.is_valid() and date_form.is_valid() and checkbox_form.is_valid():
            eod_data = getApiEod(date_form.cleaned_data['date_field'] , form.cleaned_data['ticker_choice'], checkbox_form.data.get('is_latest'))            
            data = eod_data['data']
            eod_date = ''
            for item in data:
                for key in item:
                    if key == 'date':
                        eod_date = item[key]
                        
            time = dp.parse(item['date']) # convert value to datetime object
            ftime = time.strftime("%m/%d/%Y") # format date - 01/01/2099
            return render(request, 'charts/eod_data.html', context={'eod_data': data, 'eod_date': ftime, 'page_name': 'End of Day'}) 
            #render(request, 'charts/eod_data.html', context={'eod_data': data, 'eod_date': ftime, 'page_name': 'End of Day'}) 

        else:
            messages.error(request,"Error on submit.")
            
    
    param = None
    return renderDashboard(request, param)

    """ def renderDashboard(chart_img):
        form = EodForm()
        date_form = DateForm()
        checkbox_form = EodCheckboxForm()
        conf_chart_radio_form = ChartMovingAverageRadio()
        pages_list = ['exchange', 'currency', 'ticker'] #todo - move to model
        context = { #params: page name, list of links
            'page_name': 'Dashboard',
            'pages_list': pages_list,
            'form': form,
            'date_form': date_form,
            'checkbox_form': checkbox_form,
            'conf_chart_radio_form': conf_chart_radio_form,
            'chart_img': chart_img,
        }    
        return render(request, 'charts/index.html', context=context) """

def getApiEod(eod_date, ticker, is_latest):
    fin_api = FinApi()

    try:
        query_results = Ticker.objects.get(name=ticker)
    except Ticker.DoesNotExist:
        raise Http404() #logging please
    
    symbol = query_results.symbol
    return fin_api.getEod(eod_date, symbol, is_latest)

def getApiEodLimit(limit, ticker):
    fin_api = FinApi()
    mov_avg = MovingAvg()
    #eod_limit = ''
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
    print(f'SYMBOL: {symbol}')
    print(f'LIMIT: {eod_limit}')
    
    raw = fin_api.getEodLimit(eod_limit, symbol)
    raw_data = raw['data']
    str_data = json.dumps(raw_data)
        
    svg_chart = mov_avg.BuildMovAvgChart(str_data, eod_limit)

    #data = None
    #svg_chart = mov_avg.BuildMovAvgChart(data, eod_limit)
    return svg_chart




def exchange(request):
    try:
        exchange_list = Exchange.objects.all()
        context = { #params: all records in Exchange table, page name, url name 
            'exchange_list': exchange_list,
            'page_name': 'Available Exchanges',
            'exchange_detail': 'exchange_detail',
        }       
        #raise Http404 #uncomment to test try/except
    except Exchange.DoesNotExist:
        raise Http404() #if settings DEBUG=False, browser displays: Not Found The requested resource was not found on this server. [preferred]
    return render(request, 'charts/exchange.html', context=context)

def exchange_detail(request, exchange_id):
    try:
        exchange_content = Exchange.objects.filter(id=exchange_id)
        context = { #params: iterable record, page name
            'exchange_content': exchange_content,
            'page_name': 'Exchange Details',
        }
    except Exchange.DoesNotExist:
        raise Http404()
    return render(request, 'charts/exchange_detail.html', context=context)

def currency(request):
    try:
        currency_list = Currency.objects.all()
        context = {#params: all records in Currency table, page name, url name 
            'currency_list': currency_list,
            'page_name': 'Available Currencies',
            'currency_detail': 'currency_detail',
        }
    except Currency.DoesNotExist:
        raise Http404()
    return render(request, 'charts/currency.html', context=context)

def currency_detail(request, currency_id):
    try:
        currency_content = Currency.objects.filter(id=currency_id)
        context = {#params: iterable record, page name
            'currency_content': currency_content,
            'page_name': 'Currency Details',
        }
    except Currency.DoesNotExist:
        raise Http404()
    return render(request, 'charts/currency_detail.html', context=context)

def ticker(request):
    try:
        ticker_list = Ticker.objects.all()
        context = {#params: all records in Ticker table, page name, url name 
            'ticker_list': ticker_list,
            'page_name': 'Available Tickers',
            'ticker_detail': 'ticker_detail',
        }
    except Ticker.DoesNotExist:
        raise Http404()
    return render(request, 'charts/ticker.html', context=context)

def ticker_detail(request, ticker_id):
    try:
        ticker_content = Ticker.objects.filter(id=ticker_id)
        context = {#params: iterable record, page name
            'ticker_content': ticker_content,
            'page_name': 'Ticker Details',
        }
    except Ticker.DoesNotExist:
        raise Http404()
    return render(request, 'charts/ticker_detail.html', context=context)
