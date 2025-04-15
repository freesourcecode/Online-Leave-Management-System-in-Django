from django.db import models
from employee.models import *
from datetime import datetime

# from django.utils import timezone
# import pytz
from .choice import *


class LOPRegister(models.Model):
    empid = models.CharField(max_length=10)
    leaveid = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    leave_month = models.DateField(blank=True, null=True)
    lop = models.FloatField(default=0)
    leave_status = models.CharField(max_length=20, blank=True, null=True)


class LeaveRegister(models.Model):
    financial_year = models.CharField(max_length=10, choices=FY_CHOICE)
    empid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    # leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_LIST)
    al_opening_balance = models.FloatField(default=0)
    al_credited = models.FloatField(default=0)
    al_availed = models.FloatField(default=0)
    al_closing_balance = models.FloatField(default=0)
    sdl_opening_balance = models.FloatField(default=0)
    sdl_credited = models.FloatField(default=0)
    sdl_availed = models.FloatField(default=0)
    sdl_closing_balance = models.FloatField(default=0)
    # lop = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class LeaveBalance(models.Model):
    empid = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    financial_year = models.CharField(max_length=10, choices=FY_CHOICE)
    single_day_entitlement = models.FloatField(default=0)
    single_day_availed = models.FloatField(default=0)
    single_day_balance = models.FloatField(default=0)
    annual_entitlement = models.FloatField(default=0)
    annual_availed = models.FloatField(default=0)
    annual_balance = models.FloatField(default=0)

    def __str__(self):
        return self.name


class LeaveApplication(models.Model):
    empid = models.CharField(max_length=10)  # models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)  # models.ForeignKey(Company, on_delete=models.CASCADE)
    reporting_manager_empid = models.CharField(max_length=10, blank=True, null=True)
    tenure_month = models.IntegerField(default=0)
    applied_on = models.DateTimeField(default=datetime.now(), null=True)
    leave_type = models.CharField(max_length=50)
    leave_start = models.DateField()
    leave_end = models.DateField()
    leave_for = models.CharField(max_length=20)
    days = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    paid_leave = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    unpaid_leave = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    reason = models.CharField(max_length=100, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True, help_text="Maximum Limit is 200 Characters")
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, null=True)
    status_update_by = models.CharField(max_length=50, null=True, blank=True)
    status_update_on = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=APPROVE_CATEGORY, null=True)
    manager_remarks = models.CharField(max_length=200, blank=True, null=True, help_text="Maximum Limit is 200 Characters")
    # action_by = models.CharField(max_length=100)
    # action_date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.name + " - " + self.company


class LeaveApplicationDetails(models.Model):
    transid = models.IntegerField(null=True, blank=True)
    empid = models.CharField(max_length=10)  # models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)  # models.ForeignKey(Company, on_delete=models.CASCADE)
    tenure_month = models.IntegerField(default=0)
    applied_on = models.DateTimeField(default=datetime.now(), null=True)
    leave_month = models.DateField()
    leave_type = models.CharField(max_length=50)
    leave_start = models.DateField()
    leave_end = models.DateField()
    leave_for = models.CharField(max_length=20)
    days = models.FloatField(null=True, blank=True, default=0)
    remarks = models.CharField(max_length=50, blank=True)
    reason = models.CharField(max_length=100, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, null=True)
    log_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name + " - " + self.applied_on.strftime('%Y-%m-%d')


class LeaveCategory(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    single_day_entitlement = models.FloatField(default=0)
    annual_entitlement = models.FloatField(default=0)

    def __str__(self):
        return self.name


class LeaveType(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class LeaveReason(models.Model):
    leave_reason = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.leave_reason


class HolidayList(models.Model):
    financial_year = models.CharField(max_length=10, choices=FY_CHOICE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_type = models.CharField(max_length=50, choices=HOLIDAY_TYPE_CHOICE)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.event_name + '-' + self.location


class FY(models.Model):
    financial_year = models.CharField(max_length=10, unique=True, primary_key=True)
    set_current = models.CharField(choices=(('YES', 'YES'), ('NO', 'NO')), max_length=3)

    def __str__(self):
        return self.financial_year
