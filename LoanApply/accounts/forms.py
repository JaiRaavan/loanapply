from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('name', 'email', 'phone', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['phone'].required = True
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})