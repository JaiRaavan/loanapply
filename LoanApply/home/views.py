from django.shortcuts import render
from home.forms import ProfileForm, FinancialProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from home.models import UserProfile, CibilData, BankData, FinancialProfile
from home.forms import CibilDataForm, BankDataForm

# Create your views here.
def home_page(request):
    return render(request, 'home/home.html', context={})


@login_required
def profile_page(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Explicitly create the UserProfile with required fields
        profile = UserProfile.objects.create(
            user=request.user,
            name="",
            email=request.user.email, 
            phone="",
            age=18,
            address=""
        )
    
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Ensure all required fields are filled before saving
            profile = form.save(commit=False)
            profile.user = request.user
            
            # Check if any of the required fields are empty (based on your form fields)
            if not all([profile.name, profile.phone, profile.address]):
                messages.warning(request, "All fields are required. Please fill in all details.")
                return render(request, "home/profile.html", context={"form": form})
            
            request.session['application_id'] = profile.id
            profile.save()
            
            messages.success(request, "Profile updated successfully!")
            return HttpResponseRedirect(reverse('home:financial'))
        else:
            messages.warning(request, "Details are invalid. Please try again.")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, "home/profile.html", context={"form": form})



@login_required
def financial_page(request):
    form = FinancialProfileForm()
    
    if request.method == "POST":
        form = FinancialProfileForm(request.POST)
        
        if form.is_valid():
            # Ensure all required fields are filled before saving
            details = form.save(commit=False)
            details.user = request.user
            
            # Check if any required field is missing
            required_fields = ['monthly_income', 'requested_loan_amount', 'tenure']  # Replace with your actual field names
            missing_fields = [field for field in required_fields if not getattr(details, field)]
            
            if missing_fields:
                messages.warning(
                    request,
                    f"The following fields are required and must be filled: {', '.join(missing_fields)}"
                )
                return render(request, "home/financial.html", context={"form": form})
            
            details.save()
            
            messages.success(request, "Successfully entered financial details!")
            return HttpResponseRedirect(reverse('home:cibilbank_form'))
        else:
            messages.warning(request, "Some details are invalid. Please correct them.")
    
    return render(request, "home/financialform.html", context={"form": form})
    

@login_required
def cibilbank_form(request):

    # Fetch the applicant's UserProfile object
    applicant = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        # Bind the forms with POST data
        cibil_form = CibilDataForm(request.POST)
        bank_form = BankDataForm(request.POST)

        # Validate both forms
        if cibil_form.is_valid() and bank_form.is_valid():
            # Save CIBIL Data
            cibil_data = cibil_form.save(commit=False)
            cibil_data.applicant = request.user
            cibil_data.save()

            # Save Bank Data
            bank_data = bank_form.save(commit=False)
            bank_data.applicant = request.user
            bank_data.save()

            # Redirect to the eligibility check page
            return HttpResponseRedirect(reverse('home:eligibility_check'))
        else:
            # Display a warning if any form is invalid
            messages.warning(
                request,
                "Please ensure all fields are filled in correctly before proceeding."
            )
    else:
        # Initialize empty forms if it's a GET request
        cibil_form = CibilDataForm()
        bank_form = BankDataForm()

    # Render the page with both forms
    return render(
        request,
        'home/cibilbank.html',
        context={
            'cibil_form': cibil_form,
            'bank_form': bank_form,
        }
    )


def eligibility_check(request):

    applicant = UserProfile.objects.get(user=request.user)
    financial_details = FinancialProfile.objects.get(user=request.user)
    cibil_data = CibilData.objects.get(applicant=request.user)
    bank_data = BankData.objects.get(applicant=request.user)

    # Calculate eligibility
    dti = float(cibil_data.current_debt) / (float(financial_details.monthly_income) * 12)
    eligible = (cibil_data.cibil_score / 900) * 50 + max(0, (1 - dti) * 30) + (
        30 if bank_data.annual_income >= 3 * financial_details.requested_loan_amount else 15
    ) >= 80

    return render(request, 'home/eligibility_check.html', {'eligible': eligible, 'applicant':applicant})