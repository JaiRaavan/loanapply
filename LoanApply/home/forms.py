from django import forms
from home.models import UserProfile, FinancialProfile, CibilData, BankData
from django.core.exceptions import ValidationError
import re

# Custom Validator for Phone Number
def validate_phone_number(value):
    if not re.match(r'^[6-9]\d{9}$', value):
        raise ValidationError('Phone number must be 10 digits, start with 6, 7, 8, or 9, and contain only numbers.')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone', 'age', 'address']
    
    # Apply the custom validator to the phone field
    phone = forms.CharField(validators=[validate_phone_number])
        
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