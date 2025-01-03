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
    financial_profiles = FinancialProfile.objects.all().order_by('-created_at')
    diction = {'financial_profiles': financial_profiles, 'title': "home page"}
    return render(request, 'home/home.html', context=diction)


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
    
    return render(request, "home/profile.html", context={"form": form, 'title': "profile page"})


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
                return render(request, "home/financial.html", context={"form": form, 'title': "Financial page"})
            
            details.save()
            
            messages.success(request, "Successfully entered financial details!")
            return HttpResponseRedirect(reverse('home:cibilbank_form'))
        else:
            messages.warning(request, "Some details are invalid. Please correct them.")
    
    return render(request, "home/financialform.html", context={"form": form, 'title': "Financial page"})
    

@login_required
def cibilbank_form(request):

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
        cibil_form = CibilDataForm()
        bank_form = BankDataForm()
        
    diction = {'cibil_form': cibil_form,'bank_form': bank_form,'title': "Cibil bank details"}
    return render(request, 'home/cibilbank.html', context=diction)

@login_required
def eligibility_check(request):
    applicant = UserProfile.objects.get(user=request.user)

    financial_details = FinancialProfile.objects.filter(user=request.user).last() 

    if not financial_details:
        messages.warning(request, "Financial profile not found. Please submit your financial details.")
        return HttpResponseRedirect(reverse('home:financial'))

    cibil_data = CibilData.objects.get(applicant=request.user)

    # Calculate eligibility
    dti = float(cibil_data.current_debt) / (float(financial_details.monthly_income) * 12)
    
    # Check eligibility using the updated logic
    eligible_score = (cibil_data.cibil_score / 900) * 50 + max(0, (1 - dti) * 30) + (
        30 if (float(financial_details.monthly_income) * 12 >= 3) * financial_details.requested_loan_amount else 15
    )
    
    # Update the 'eligible' field based on the calculated score
    financial_details.eligible = eligible_score >= 80
    financial_details.save()

    if financial_details.eligible:
        messages.success(request, "You are eligible for the loan!")
    else:
        messages.warning(request, "You are not eligible for the loan.")

    # Redirect to the home page
    return HttpResponseRedirect(reverse('home:homely'))

@login_required
def personal(request):
    profile_info = UserProfile.objects.get(user=request.user)
    financial_forms = FinancialProfile.objects.filter(user=request.user)
    diction = {"title":"personal", "profile_info":profile_info, "financial_forms":financial_forms}
    
    return render(request, "home/personal.html", context=diction)