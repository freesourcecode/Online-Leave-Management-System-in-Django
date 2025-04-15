from django.forms import ModelForm
from .models import *
from django import forms


class AddEmployeeForm(ModelForm):
    empid = forms.CharField(label='Employee ID', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID', 'name': 'empid', 'id': 'empid', 'autofocus': 'True'}), required=True, max_length=10)
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'name': 'name', 'id': 'name'}), required=True, max_length=100)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email Address', 'name': 'email', 'id': 'email'}), required=True, max_length=75)
    company = forms.ModelChoiceField(queryset=Company.objects.order_by('name').all().distinct(), label='Company', widget=forms.Select(attrs={'class': 'form-control', 'name': 'company', 'id': 'company'}), required=True)
    designation = forms.CharField(label='Designation', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation', 'name': 'designation', 'id': 'designation'}), required=True, max_length=100)
    date_of_joining = forms.DateField(label='Joining Date', widget=forms.DateInput(attrs={'class': 'form-control', 'name': 'date_of_joining', 'id': 'date_of_joining', 'data-date-format':'yyyy-mm-dd', 'placeholder': 'YYYY-MM-DD'}), required=True)
    job_location = forms.ModelChoiceField(queryset=Location.objects.order_by('job_location').all().distinct(), label='Job Location', widget=forms.Select(attrs={'class': 'form-control', 'name': 'job_location', 'id': 'job_location'}), required=True)
    employment_setup = forms.ModelChoiceField(queryset=EmploymentSetup.objects.all().distinct(), label='Employment Setup', widget=forms.Select(attrs={'class': 'form-control', 'name': 'employment_setup', 'id': 'employment_setup'}), required=True)
    gender = forms.ModelChoiceField(queryset=Gender.objects.all().distinct(), label='Gender', widget=forms.Select(attrs={'class': 'form-control', 'name': 'gender', 'id': 'gender'}), required=True)
    marital_status = forms.ModelChoiceField(queryset=MaritalStatus.objects.all().distinct(), label='Marital Status', widget=forms.Select(attrs={'class': 'form-control', 'name': 'marital_status', 'id': 'marital_status'}), required=True)
    user_type = forms.ModelChoiceField(queryset=UserType.objects.all().distinct(), label='User Type', widget=forms.Select(attrs={'class': 'form-control', 'name': 'user_type', 'id': 'user_type'}), required=True)
    weekend_day = forms.ModelChoiceField(queryset=WeekendDay.objects.all().distinct(), label='Weekend Day', widget=forms.Select(attrs={'class': 'form-control', 'name': 'weekend_day', 'id': 'weekend_day'}), required=True)
    leave_category = forms.ModelChoiceField(queryset=LeaveCategory.objects.order_by('name').all().distinct(), label='Leave Category', widget=forms.Select(attrs={'class': 'form-control', 'name': 'leave_category', 'id': 'leave_category'}), required=True)
    single_day_entitlement = forms.CharField(label='Single Day Entitlement', widget=forms.Select(attrs={'class': 'form-control', 'name': 'single_day_entitlement', 'id': 'single_day_entitlement'}), required=True)
    annual_entitlement = forms.CharField(label='Annual Entitlement', widget=forms.Select(attrs={'class': 'form-control', 'name': 'annual_entitlement', 'id': 'annual_entitlement'}), required=True)
    reporting_manager_empid = forms.CharField(label='Manager Emp ID', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emp ID', 'name': 'reporting_manager_empid', 'id': 'reporting_manager_empid'}), required=True, max_length=10)
    reporting_manager_name = forms.CharField(label='Manager Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager Name', 'name': 'reporting_manager_name', 'id': 'reporting_manager_name'}), required=True, max_length=100)
    reporting_manager_email = forms.EmailField(label='Manager Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Manager Email', 'name': 'reporting_manager_email', 'id': 'reporting_manager_email'}), required=True, max_length=75)
    date_of_leaving = forms.DateField(label='Date of Leaving', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'value': '1900-01-01', 'readonly': 'form-control', 'name': 'date_of_leaving', 'data-date-format':'yyyy-mm-dd', 'id': 'date_of_leaving'}), required=False)
    employee_status = forms.ModelChoiceField(queryset=EmployeeStatus.objects.all().distinct(), label='Employee Status', widget=forms.Select(attrs={'class': 'form-control', 'name': 'employee_status', 'id': 'employee_status'}), required=True)

    class Meta:
        model = EmployeeDetails
        fields = '__all__'
        exclude = ['userid']
