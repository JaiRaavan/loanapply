from django.contrib import admin
from home.models import UserProfile, FinancialProfile, CibilData, BankData


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FinancialProfile)
admin.site.register(CibilData)
admin.site.register(BankData)