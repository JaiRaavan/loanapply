from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.utils.timezone import now

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True) 
    phone = models.CharField(max_length=15, unique=True) 
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(120)], blank=True, null=True, default=18)
    address = models.TextField(max_length=200) 

    def __str__(self):
        return self.name
    
    
class FinancialProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_profile')
    monthly_income = models.DecimalField(max_digits=15, decimal_places=2) 
    requested_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)  
    tenure = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    eligible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}'s Financial Profile"
    

class CibilData(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cibil_profile")
    cibil_score = models.PositiveIntegerField()
    current_debt = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        CibilData.objects.filter(applicant=self.applicant).delete()
        # Save the new record
        super().save(*args, **kwargs)
    
class BankData(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_profile")
    employer_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    
    
@receiver(pre_save, sender=BankData)
def set_bank_data_defaults(sender, instance, **kwargs):
    # Set employer_name to the name from UserProfile if not already set
    if not instance.employer_name:
        instance.employer_name = instance.applicant.profile.name  
        
    financial_profile = instance.applicant.financial_profile.first()
    if financial_profile:
        instance.annual_income = financial_profile.monthly_income * 12