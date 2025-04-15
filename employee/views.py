from django.shortcuts import render
from django.http import HttpResponseRedirect
from applyleave.models import LeaveCategory
from .forms import AddEmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import re
from employee.models import *
from django.contrib.auth.models import User
from accounts.views import *


@login_required(login_url='/login/')
def add_employee_view(request):
    context = {
        'form': AddEmployeeForm(),
        'obj_Company': Company.objects.all(),
        'obj_LeaveCategory': LeaveCategory.objects.all().order_by('name'),
        'obj_Job_Location': Location.objects.all(),
        'obj_Emp_Setup': EmploymentSetup.objects.all(),
        'obj_Gender': Gender.objects.all(),
        'obj_Marital_Status': MaritalStatus.objects.all(),
        'obj_User_Type': UserType.objects.all(),
        'obj_Weekend_Day': WeekendDay.objects.all(),
        'obj_Emp_Status': EmployeeStatus.objects.all(),
    }
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            # form.save()
            empid = re.sub(' +', ' ', request.POST.get('empid', '')).strip()
            name = re.sub(' +', ' ', request.POST.get('name', '')).strip()
            email = re.sub(' +', ' ', request.POST.get('email', '')).strip()
            company = request.POST.get('company', '')
            designation = re.sub(' +', ' ', request.POST.get('designation', '')).strip()
            date_of_joining = request.POST.get('date_of_joining', '')
            job_location = request.POST.get('job_location', '')
            employment_setup = request.POST.get('employment_setup', '')
            gender = request.POST.get('gender', '')
            marital_status = request.POST.get('marital_status', '')
            user_type = request.POST.get('user_type', '')
            weekend_day = request.POST.get('weekend_day', '')
            leave_category = request.POST.get('leave_category', '')
            single_day_entitlement = request.POST.get('single_day_entitlement', '')
            annual_entitlement = request.POST.get('annual_entitlement', '')
            reporting_manager_empid = re.sub(' +', ' ', request.POST.get('reporting_manager_empid', '')).strip()
            reporting_manager_name = re.sub(' +', ' ', request.POST.get('reporting_manager_name', '')).strip()
            reporting_manager_email = re.sub(' +', ' ', request.POST.get('reporting_manager_email', '')).strip()
            date_of_leaving = request.POST.get('date_of_leaving', '1900-01-01')
            employee_status = request.POST.get('employee_status')

            emp_obj = EmployeeDetails(empid=empid, name=name, email=email, company=company,
                                      designation=designation, date_of_joining=date_of_joining,
                                      job_location=job_location, employment_setup=employment_setup,
                                      gender=gender, marital_status=marital_status, user_type=user_type,
                                      weekend_day=weekend_day, leave_category=leave_category,
                                      single_day_entitlement=single_day_entitlement,
                                      annual_entitlement=annual_entitlement,
                                      reporting_manager_empid=reporting_manager_empid,
                                      reporting_manager_name=reporting_manager_name,
                                      reporting_manager_email=reporting_manager_email,
                                      date_of_leaving=date_of_leaving,
                                      employee_status=employee_status)

            emp_obj.save()
            context = {
                'save_message': 'Data has been Saved. !!!'
            }
            return render(request, 'add_employee.html', context)
        else:
            context = {
                'form': AddEmployeeForm(request.POST),
                'obj_Company': Company.objects.all(),
                'obj_LeaveCategory': LeaveCategory.objects.all().order_by('name'),
                'obj_Job_Location': Location.objects.all(),
                'obj_Emp_Setup': EmploymentSetup.objects.all(),
                'obj_Gender': Gender.objects.all(),
                'obj_Marital_Status': MaritalStatus.objects.all(),
                'obj_User_Type': UserType.objects.all(),
                'obj_Weekend_Day': WeekendDay.objects.all(),
                'obj_Emp_Status': EmployeeStatus.objects.all(),
            }
            return render(request, 'add_employee.html', context)
    else:
        return render(request, 'add_employee.html', context)
    # return HttpResponseRedirect(reverse(add_employee_view), context)


def employee_list_view(request):
    context = {
        'obj_emp': EmployeeDetails.objects.all().order_by('-date_of_joining'),
    }
    return render(request, 'list_employee.html', context)


def employee_details_view(request, id=None):
    context = {}
    obj_emp = EmployeeDetails.objects.get(empid=id)
    context['obj_emp'] = obj_emp
    return render(request, 'view_employee.html', context)


def employee_edit_view(request, id=None):
    context = {
        'form': AddEmployeeForm(),
        'obj_Company': Company.objects.all,
        'obj_LeaveCategory': LeaveCategory.objects.all().order_by('name'),
        'obj_Job_Location': Location.objects.all(),
        'obj_Emp_Setup': EmploymentSetup.objects.all(),
        'obj_Gender': Gender.objects.all(),
        'obj_Marital_Status': MaritalStatus.objects.all(),
        'obj_User_Type': UserType.objects.all(),
        'obj_Weekend_Day': WeekendDay.objects.all(),
        'obj_Emp_Status': EmployeeStatus.objects.all(),
    }
    obj_emp = EmployeeDetails.objects.get(empid=id)
    context['obj_emp'] = obj_emp
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, instance=obj_emp)
        context['form'] = form
        if form.is_valid():
            form.save()
            context['form'] = AddEmployeeForm(request.POST, instance=obj_emp)
            context['save_message'] = 'Updated Successfully !!!'
            return render(request, 'edit_employee.html', context)
        else:
            context['save_message'] = 'Invalid Input !!!'
            return render(request, 'edit_employee.html', context)
    return render(request, 'edit_employee.html', context)


def employee_delete_view(request, id=None):
    context = {
        'form': AddEmployeeForm(),
        'obj_Company': Company.objects.all,
        'obj_LeaveCategory': LeaveCategory.objects.all().order_by('name'),
        'obj_Job_Location': Location.objects.all(),
        'obj_Emp_Setup': EmploymentSetup.objects.all(),
        'obj_Gender': Gender.objects.all(),
        'obj_Marital_Status': MaritalStatus.objects.all(),
        'obj_User_Type': UserType.objects.all(),
        'obj_Weekend_Day': WeekendDay.objects.all(),
        'obj_Emp_Status': EmployeeStatus.objects.all(),
    }
    obj_emp = EmployeeDetails.objects.get(empid=id)
    context['obj_emp'] = obj_emp
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, instance=obj_emp)
        context['form'] = form
        obj_emp.delete()
        context['save_message'] = 'Deleted Successfully !!!'
        return render(request, 'delete_employee.html', context)
    return render(request, 'delete_employee.html', context)


@login_required(login_url='/login/')
def profile_view(request):
    context = {}
    user_obj = User.objects.get(email=request.user.email)
    obj_emp = EmployeeDetails.objects.get(email=user_obj.email)
    context['obj_emp'] = obj_emp
    return render(request, 'view_profile.html', context)

