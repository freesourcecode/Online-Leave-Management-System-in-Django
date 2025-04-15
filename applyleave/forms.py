from django import forms
from django.forms import ModelForm
from .models import *
from .choice import *


class LeaveApplicationForm(forms.ModelForm):
    leave_type = forms.ModelChoiceField(queryset=LeaveType.objects.all(), label='Leave Type', required=True, widget=forms.Select(attrs={'class': 'form-control', 'autofocus': 'True'}, choices=LEAVE_TYPE_LIST))
    leave_start = forms.DateField(label="From Date", required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'date_start', 'name': 'leave_start', 'data-date-format':'yyyy-mm-dd'}))
    leave_end = forms.DateField(label='To', required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'date_end', 'name': 'leave_end', 'data-date-format':'yyyy-mm-dd'}))
    leave_for = forms.CharField(label='Leave For', required=True, widget=forms.Select(attrs={'class': 'form-control', 'id': 'leave_for', 'name': 'leave_for'}, choices=LEAVE_FOR_CHOICE))
    days = forms.CharField(label='Days', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'days', 'name': 'days', 'value':'0' }))
    reason = forms.ModelChoiceField(queryset=LeaveReason.objects.order_by('leave_reason').all().distinct(), label='Leave Reason', required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    comments = forms.CharField(label='Comments', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = LeaveApplication
        fields = '__all__'
        exclude = ['empid', 'name', 'company', 'tenure_month', 'applied_on', 'status',
                   'paid_leave', 'unpaid_leave', 'status_update_by', 'status_update_on', 'category']


class LeaveRegisterForm(forms.ModelForm):
    financial_year = forms.ModelChoiceField(label="Financial Year", queryset=FY.objects.all(), widget=forms.Select(attrs={'class':'form-control', 'name':'financial_year'}))
    empid = forms.CharField(label='Employee ID', max_length=10,  widget=forms.TextInput(attrs={'class':'form-control', 'name': 'empid'}))
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'name': 'name'}))
    company = forms.CharField(label='Company', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'name': 'company'}))
    # tenure_month = forms.IntegerField(label='Tenure Month', widget=forms.TextInput(attrs={'class':'form-control'}))
    # leave_type = forms.ModelChoiceField(label='Leave Type', queryset=LeaveType.objects.all(), widget=forms.Select(attrs={'class':'form-control', 'name':'leave_type'}))
    al_opening_balance = forms.DecimalField(label='Opening Balance', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    al_credited = forms.DecimalField(label='Credit Leave', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    al_availed = forms.DecimalField(label='Availed', max_digits=5, decimal_places=2,widget=forms.TextInput(attrs={'class':'form-control'}))
    al_closing_balance = forms.DecimalField(label='Closing Balance', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    sdl_opening_balance = forms.DecimalField(label='Opening Balance', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    sdl_credited = forms.DecimalField(label='Credit Leave', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    sdl_availed = forms.DecimalField(label='Availed', max_digits=5, decimal_places=2,widget=forms.TextInput(attrs={'class':'form-control'}))
    sdl_closing_balance = forms.DecimalField(label='Closing Balance', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))

    # lop = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = LeaveRegister
        fields = '__all__'
        #exclude = ['lop']


class ManagerActionForm(forms.ModelForm):
    manager_action = forms.ChoiceField(label="Manager Action", choices=STATUS_CHOICE, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    category = forms.ChoiceField(label='Category', choices=APPROVE_CATEGORY, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    manager_remarks = forms.CharField(label='Manager Remarks', max_length=200, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = LeaveApplication
        fields = ['status', 'category', 'manager_remarks']
