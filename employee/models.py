from django.db import models
from django.contrib.auth.models import User
from applyleave.models import LeaveCategory
from datetime import datetime


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class EmployeeDetails(models.Model):
    empid = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=75, unique=True)
    company = models.CharField(max_length=50)  # models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100)
    date_of_joining = models.DateField(null=True, blank=True)
    job_location = models.CharField(max_length=100, default='Goa')
    employment_setup = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20, default='User')
    weekend_day = models.CharField(max_length=2, default=2)
    leave_category = models.CharField(max_length=10)  # models.ForeignKey(LeaveCategory, on_delete=models.CASCADE)
    single_day_entitlement = models.CharField(max_length=5, default=0)
    annual_entitlement = models.CharField(max_length=5, default=0)
    reporting_manager_empid = models.CharField(max_length=10)
    reporting_manager_name = models.CharField(max_length=100)
    reporting_manager_email = models.EmailField(max_length=75)
    date_of_leaving = models.DateField(null=True, blank=True)
    employee_status = models.CharField(max_length=10, default='Active')
    userid = models.IntegerField(null=True, blank=True)
    # password = models.CharField(null=True, blank=True, max_length=128)

    def __str__(self):
        return self.name  # + " - " + self.company


class Location(models.Model):
    job_location = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.job_location


class EmploymentSetup(models.Model):
    employment_setup = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return self.employment_setup


class Gender(models.Model):
    gender = models.CharField(max_length=20, unique=True, primary_key=True)

    def __str__(self):
        return self.gender


class MaritalStatus(models.Model):
    marital_status = models.CharField(max_length=20, unique=True, primary_key=True)

    def __str__(self):
        return self.marital_status


class UserType(models.Model):
    user_type = models.CharField(max_length=20, unique=True, primary_key=True)

    def __str__(self):
        return self.user_type


class WeekendDay(models.Model):
    weekend_day = models.CharField(max_length=2, unique=True, primary_key=True)

    def __str__(self):
        return self.weekend_day


class EmployeeStatus(models.Model):
    employee_status = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return self.employee_status

