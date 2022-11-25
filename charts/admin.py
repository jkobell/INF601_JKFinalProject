# INF601 - Advanced Programming in Python
# James Kobell
# Final Project
from django.contrib import admin

# Register your models here.
from .models import Ticker
from .models import Chart
from .models import Exchange
from .models import Timezone
from .models import Currency
from .models import Intraday
from .models import Accounts
from .models import UsersCharts

admin.site.register(Ticker)
admin.site.register(Chart)
admin.site.register(Exchange)
admin.site.register(Timezone)
admin.site.register(Currency)
admin.site.register(Intraday)
admin.site.register(Accounts)
admin.site.register(UsersCharts)



