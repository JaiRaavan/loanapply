from django import forms
from home.models import UserProfile, FinancialProfile, CibilData, BankData

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone', 'age', 'address']
        
class FinancialProfileForm(forms.ModelForm):
    class Meta:
        model = FinancialProfile
        fields = ['monthly_income', 'requested_loan_amount', 'tenure']
        
class CibilDataForm(forms.ModelForm):
    class Meta:
        model = CibilData
        fields = ['cibil_score', 'current_debt']
        
class BankDataForm(forms.ModelForm):
    class Meta:
        model = BankData
        fields = ['employer_name', 'designation', 'annual_income']