from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from employee.models import *
import datetime
from datetime import datetime, timedelta
from django.db.models import Max
from django.views.generic import View
import re
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q


def email(request, leave_type, leave_start, leave_end, days, reason, comments, to, subject, html_content):
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def email_notification(to, subject, html_content):
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@login_required(login_url="/login/")
def check_leave_balance_view(request):
    context = {
        # 'obj_leave': LeaveBalance.objects.all(),
    }
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    obj_fy = FY.objects.get(set_current='YES')
    leave_register = LeaveRegister.objects.filter(financial_year=obj_fy.financial_year, empid=obj_emp.empid)
    context['leave_register'] = leave_register
    return render(request, 'leave_balance.html', context)


def holiday_list_view(request):
    context = {
        'obj_holiday': HolidayList.objects.order_by('event_date').all(),
        'obj_fy': FY.objects.get(set_current='YES'),
    }
    return render(request, 'holiday_list.html', context)


# ------ Check if leave already applied -----------------
def is_leave_applied(request, leave_start, leave_end):
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    days_count = (leave_end.date() - leave_start.date()).days + 1
    applied_leave = 0
    for leave in range(days_count):
        leave_start_new = leave_start + timedelta(days=leave)
        leave_count = LeaveApplicationDetails.objects.filter(empid=obj_emp.empid, leave_start=leave_start_new).filter(Q(status='PENDING') | Q(status='APPROVED')).count()
        if leave_count >= 1:
            applied_leave += 1
        else:
            applied_leave += 0
    return applied_leave


# ------ Create dict for leaves -----------------
def create_dict_for_leaves(request, leave_start, leave_end, leave_for):
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    leave_start = datetime.strptime(str(leave_start).rsplit(" ")[0], "%Y-%m-%d")
    leave_end = datetime.strptime(str(leave_end).rsplit(" ")[0], "%Y-%m-%d")
    days_count = (leave_end.date() - leave_start.date()).days + 1
    my_leaves_dict = {}
    days = 0

    for leave in range(days_count):
        leave_start_new = leave_start + timedelta(days=leave)
        leave_for_new = request.POST.get('leave_for_' + str(str(leave_start_new).rsplit(" ")[0]))
        if leave_for_new is None:
            leave_for_new = leave_for
        else:
            pass

        if leave_for_new == 'Full Day':
            days = 1
            leave_for = leave_for_new
        elif leave_for_new is not 'Full Day':
            days = 0.5
            leave_for = leave_for_new

        holiday_count = HolidayList.objects.filter(event_date=leave_start_new).count()
        if obj_emp.weekend_day == '2':
            if leave_start_new.weekday() == 5 or leave_start_new.weekday() == 6:
                remarks = 'Weekend'
                days = 0
            elif holiday_count >= 1:
                remarks = 'Holiday'
                days = 0
            else:
                remarks = 'Working Day'
                days = days
        else:
            if leave_start_new.weekday() == 6:
                remarks = 'Weekend'
                days = 0
            elif holiday_count >= 1:
                remarks = 'Holiday'
                days = 0
            else:
                remarks = 'Working Day'
                days = days

        my_leaves_dict.update({leave_start_new: {'leave_start': leave_start_new, 'leave_end': leave_start_new, 'leave_for': leave_for, 'days': days, 'remarks': remarks}})

    return my_leaves_dict


# @login_required(login_url="/login/")
class ApplyLeaveView(View):
    template_name = 'applyleave.html'

    def get(self, request):
        context = {'form': LeaveApplicationForm}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        form = LeaveApplicationForm(request.POST)
        leave_start = datetime.strptime(request.POST.get('leave_start'), "%Y-%m-%d")
        leave_end = datetime.strptime(request.POST.get('leave_end'), "%Y-%m-%d")
        leave_for = request.POST.get('leave_for')
        print("func", leave_for)
        if form.is_valid():
            if leave_start > leave_end:
                context['error_message'] = 'Invalid From Date !!!'
                context['form'] = LeaveApplicationForm(request.POST)
                return render(request, self.template_name, context)
            else:
                # ------ Check if leave already applied -----------------
                if is_leave_applied(request, leave_start, leave_end) >= 1:
                    context['form'] = LeaveApplicationForm(request.POST)
                    context['error_message'] = 'Leave already applied. !!!'
                    return render(request, self.template_name, context)

                else:
                    days_count = (leave_end.date() - leave_start.date()).days + 1
                    context['obj_days_count'] = days_count
                    dict = create_dict_for_leaves(request, leave_start, leave_end, leave_for)
                    context['obj_leave_date_list'] = dict
                    global list_of_leave_date
                    list_of_leave_date = dict
                    global leave_review_form
                    leave_review_form = LeaveApplicationForm(request.POST)
                    context['form'] = leave_review_form
                    return render(request, self.template_name, context)
        else:
            context['form'] = leave_review_form
            return render(request, self.template_name, context)


class LeaveAppReview(View):
    template_name = 'applyleave.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': leave_review_form, 'obj_leave_date_list': list_of_leave_date})

    def post(self, request):
        context = {}
        obj_emp = EmployeeDetails.objects.get(email=request.user.email)
        context['form'] = leave_review_form
        context['obj_leave_date_list'] = list_of_leave_date
        leave_start = request.POST.get('leave_start')
        leave_start_get = datetime.strptime(str(str(leave_start).rsplit(" ")[0]), "%Y-%m-%d")
        leave_end = request.POST.get('leave_end')
        leave_end = datetime.strptime(leave_end, "%Y-%m-%d")
        days_count = (leave_end.date() - leave_start_get.date()).days + 1
        leave_for = request.POST.get('leave_for_' + str(str(leave_start).rsplit(" ")[0]))
        new_dict = create_dict_for_leaves(request, leave_start, leave_end, leave_for)
        leavecount = 0
        for key, value in new_dict.items():
            leavecount = leavecount + value["days"]

        # --------- Check leave balance -----------
        obj_emp = EmployeeDetails.objects.get(email=request.user.email)
        obj_fy = FY.objects.get(set_current='YES')
        leave_register = LeaveRegister.objects.get(financial_year=obj_fy.financial_year, empid=obj_emp.empid)

        global paid_leave
        global unpaid_leave

        if request.POST.get('leave_type') == 'Single Day':
            if leavecount <= leave_register.sdl_closing_balance:
               paid_leave = leavecount
               unpaid_leave = 0
            else:
                paid_leave = leave_register.sdl_closing_balance
                unpaid_leave = float(leavecount) - float(leave_register.sdl_closing_balance)
        else:
            if leavecount <= leave_register.al_closing_balance:
                paid_leave = leavecount
                unpaid_leave = 0
            else:
                paid_leave = leave_register.al_closing_balance
                unpaid_leave = float(leavecount) - float(leave_register.al_closing_balance)

        context['paid_leave'] = paid_leave
        context['unpaid_leave'] = unpaid_leave

        global list_of_leave_details
        list_of_leave_details = new_dict
        global total_leave_count
        total_leave_count = leavecount
        context['obj_leave_date_list'] = list_of_leave_details
        context['total_leave'] = total_leave_count
        next = request.POST.get('next', '/')
        return render(request, 'applyleave_step_3.html', context)


class LeaveAppSubmit(View):
    template_name = 'applyleave_step_3.html'

    def get(self, request):
        context = {
            'form': leave_review_form,
            'obj_leave_date_list': list_of_leave_details,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        obj_emp = EmployeeDetails.objects.get(email=request.user.email)
        context['form'] = leave_review_form
        context['paid_leave'] = paid_leave
        context['unpaid_leave'] = unpaid_leave
        empid = obj_emp.empid
        name = obj_emp.name
        company = obj_emp.company
        reporting_manager_empid = obj_emp.reporting_manager_empid
        applied_on = datetime.now()  # datetime.datetime.now()
        leave_type = request.POST.get('leave_type')
        leave_start = request.POST.get('leave_start')
        leave_start_new = datetime.strptime(leave_start, "%Y-%m-%d")
        leave_end = request.POST.get('leave_end')
        leave_end = datetime.strptime(leave_end, "%Y-%m-%d")
        leave_end_new = str(leave_end).split(" ")[0]
        leave_for = request.POST.get('leave_for')
        leave_month = datetime(leave_start_new.year, leave_start_new.month, 1)
        reason = request.POST.get('reason')  # constant
        comments = request.POST.get('comments')  # constant
        status = 'PENDING'  # constant
        # Calculating tenure months between DOJ and Leave Start Date
        emp_doj = obj_emp.date_of_joining
        tenure_month = (leave_start_new.year - emp_doj.year) * 12 + leave_start_new.month - emp_doj.month
        # ------ Check if leave already applied -----------------
        if is_leave_applied(request, leave_start_new, leave_end) >= 1:
            context['form'] = LeaveApplicationForm(request.POST)
            context['total_leave'] = total_leave_count
            context['error_message'] = 'Leave already applied. !!!'
            return render(request, 'applyleave_step_3.html', context)

        if leave_type == "Annual" and total_leave_count < 3:
            context['error_message'] = 'Minimum Annual Leave Should be 3 days !!!'
            context['total_leave'] = total_leave_count
            return render(request, 'applyleave_step_3.html', context)

        if leave_type == "Single Day" and total_leave_count >= 3:
            context['error_message'] = 'Single Day Leave Must be less than 3 days. !!!'
            context['total_leave'] = total_leave_count
            return render(request, 'applyleave_step_3.html', context)
        else:

            obj_leave_app = LeaveApplication(empid=empid, name=name, company=company,reporting_manager_empid=reporting_manager_empid,
                                             tenure_month=tenure_month, applied_on=applied_on,
                                             leave_type=leave_type, leave_start=leave_start,
                                             leave_end=leave_end, leave_for=leave_for,
                                             days=total_leave_count, paid_leave=paid_leave, unpaid_leave=unpaid_leave, reason=reason, comments=comments, status=status)
            obj_leave_app.save()

            transid = obj_leave_app.pk

            for key, value in list_of_leave_details.items():
                obj_leave_app = LeaveApplicationDetails(transid=transid, empid=empid, name=name, company=company,
                                                        tenure_month=tenure_month, applied_on=applied_on,
                                                        leave_month=leave_month,
                                                        leave_type=leave_type, leave_start=value.get("leave_start"),
                                                        leave_end=value.get("leave_end"),
                                                        leave_for=value.get("leave_for"),
                                                        days=value.get("days"), remarks=value.get("remarks"), reason=reason,
                                                        comments=comments, status=status, log_status='')

                obj_leave_app.save()

            # ------ Update in leave register -----------
            current_fy = FY.objects.get(set_current='YES')
            current_fy = current_fy.financial_year
            leave_register = LeaveRegister.objects.get(financial_year=current_fy, empid=empid)
            if leave_type == "Annual":
                leave_register.al_availed = (float(leave_register.al_availed) + float(total_leave_count))
                leave_register.al_closing_balance = (float(leave_register.al_closing_balance) - float(total_leave_count))
            elif leave_type == "Single Day":
                leave_register.sdl_availed = (float(leave_register.sdl_availed) + float(total_leave_count))
                leave_register.sdl_closing_balance = (float(leave_register.sdl_closing_balance) - float(total_leave_count))
            else:
                pass
            leave_register.save()
            context['total_leave'] = total_leave_count
            days = total_leave_count
            # --- sending email to manager -------------
            to = obj_emp.reporting_manager_email
            rpt_mgr_name = obj_emp.reporting_manager_name.split(" ")[0]
            subject = f'#{transid} Leave Request for {leave_type} Leave - applied by - {obj_emp.name}'
            context['save_message'] = 'Leave Applied Successfully. Wait for your manager approval !!!'
            html_content = f"Dear {rpt_mgr_name}, <br><p>{obj_emp.name} applied for leave. Kindly login to Leave Portal and approve the same. <br> Leave Details : <br> Leave Type: <strong>{leave_type}</strong><br> Leave Start : <strong>{leave_start}</strong><br> Leave End : <strong> {leave_end_new} </strong> <br> Days Count : <strong> {days} </strong> <br> Reason : <strong> {reason} </strong> <br> Remarks : {comments} <br> Status : <strong> PENDING </strong> </p>"
            email(request, leave_type, leave_start, leave_end_new, days, reason, comments, to, subject, html_content)
            # -------------------------------------------
            # --- sending email to user -----------------
            subject = f'#{transid} Notification: Leave Request - {leave_type} Leave'
            to = request.user.email
            fname = obj_emp.name.split(" ")[0]
            html_content = f"Dear { fname }, <br> Your leave request has been successfully sent to your reporting manager. <br> Leave Details : <br> Leave Type: <strong>{leave_type}</strong><br> Leave Start : <strong>{leave_start}</strong><br> Leave End : <strong> {leave_end_new} </strong> <br> Days Count : <strong> {days} </strong> <br> Reason : <strong> {reason} </strong> <br> Remarks : {comments} <br> Status : <strong> PENDING </strong> </p>"
            email(request, leave_type, leave_start, leave_end_new, days, reason, comments, to, subject, html_content)
            return render(request, 'applyleave_step_finish.html', context)


def my_leave_view(request, id=None):
    context = {}
    obj_leave_app = LeaveApplication.objects.get(id=id)
    context['obj_leave_app'] = obj_leave_app
    leave_details = LeaveApplicationDetails.objects.filter(transid=id)
    full_day = LeaveApplicationDetails.objects.filter(transid=id, leave_for='Full Day', remarks='Working Day').count()
    half_day = (obj_leave_app.days - full_day) * 2
    context['full_day'] = float(full_day)
    context['half_day'] = float(half_day)
    context['leave_details'] = leave_details
    return render(request, 'myleave_view.html', context)


def my_leave_cancel(request, id=None):
    context = {}
    leave_app = LeaveApplication.objects.get(id=id)
    context['obj_leave_app'] = LeaveApplication.objects.get(id=id)
    leave_details = LeaveApplicationDetails.objects.filter(transid=id)
    context['leave_details'] = leave_details
    full_day = LeaveApplicationDetails.objects.filter(transid=id, leave_for='Full Day', remarks='Working Day').count()
    half_day = (leave_app.days - full_day) * 2
    context['full_day'] = float(full_day)
    context['half_day'] = float(half_day)
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    if request.method == 'POST':
        # ------ Update in leave register -----------
        current_fy = FY.objects.get(set_current='YES')
        current_fy = current_fy.financial_year
        leave_register = LeaveRegister.objects.get(financial_year=current_fy, empid=obj_emp.empid)
        if leave_app.leave_type == "Annual":
            leave_register.al_availed = (float(leave_register.al_availed) - float(leave_app.paid_leave))
            leave_register.al_closing_balance = (float(leave_register.al_closing_balance) + float(leave_app.paid_leave))
        elif leave_app.leave_type == "Single Day":
            leave_register.sdl_availed = (float(leave_register.sdl_availed) - float(leave_app.paid_leave))
            leave_register.sdl_closing_balance = (float(leave_register.sdl_closing_balance) + float(leave_app.paid_leave))
        else:
            pass
        leave_register.save()
        leave_app.status = "CANCELLED"
        leave_app.save()
        leave_app_details = LeaveApplicationDetails.objects.filter(transid=id).update(status="CANCELLED")

        context['save_message'] = 'Leave Request has been cancelled Successfully !!!'
        # --- sending email to manager -------------
        to = obj_emp.reporting_manager_email
        rpt_mgr_name = obj_emp.reporting_manager_name.split(" ")[0]
        subject = f'#Leave ID #{id} for {leave_app.leave_type} Leave - cancelled by - {obj_emp.name}'
        html_content = f"Dear {rpt_mgr_name}, <br><p>Leave Request for {leave_app.leave_type} Leave from <strong> {leave_app.leave_start} </strong> to <strong> {leave_app.leave_end} </strong> has been cancelled by {obj_emp.name}."
        email_notification(to, subject, html_content)
        # -------------------------------------------
        # --- sending email to user -----------------
        subject = f'Notification: Leave ID #{id} for {leave_app.leave_type} Leave - cancelled'
        to = request.user.email
        fname = obj_emp.name.split(" ")[0]
        html_content = f"Dear {fname}, <br><p> Your leave request has been cancelled.</p>"
        email_notification(to, subject, html_content)
        return render(request, 'myleave_cancel.html', context)
    return render(request, 'myleave_cancel.html', context)


def team_leave_view(request, id=None):
    context = {
        'form': ManagerActionForm()
    }
    global leave_id
    leave_id = id
    leave_details = LeaveApplicationDetails.objects.filter(transid=id)
    obj_leave_app = LeaveApplication.objects.get(id=id)
    context['obj_leave_app'] = obj_leave_app
    full_day = LeaveApplicationDetails.objects.filter(transid=id, leave_for='Full Day', remarks='Working Day').count()
    half_day = (obj_leave_app.days - full_day) * 2
    context['full_day'] = float(full_day)
    context['half_day'] = float(half_day)
    context['leave_details'] = leave_details
    return render(request, 'teamleave_view.html', context)


def leave_manager_action(request):
    context = {
        'form': ManagerActionForm()
    }
    leave_app = LeaveApplication.objects.get(id=leave_id)
    context['obj_leave_app'] = leave_app
    # context['leave_id'] = leave_id
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    obj_user = EmployeeDetails.objects.get(empid=leave_app.empid)
    leave_details = LeaveApplicationDetails.objects.filter(transid=leave_id)
    full_day = LeaveApplicationDetails.objects.filter(transid=leave_id, leave_for='Full Day', remarks='Working Day').count()
    half_day = (leave_app.days - full_day) * 2
    context['full_day'] = float(full_day)
    context['half_day'] = float(half_day)
    context['leave_details'] = leave_details
    form = ManagerActionForm()
    if request.method == 'POST':
        form = ManagerActionForm(request.POST)
        new_status = request.POST.get("manager_action")
        category = request.POST.get("category")
        manager_remarks = request.POST.get("manager_remarks")
        if form.is_valid:
            if category == 'Choose...' or new_status == 'Choose...':
                context['error_message'] = 'Please Select !!!'
                context['form'] = ManagerActionForm(request.POST)
                return render(request, 'teamleave_view.html', context)
            elif new_status == "APPROVED":
                if leave_app.unpaid_leave == 0:
                        LeaveApplication.objects.filter(id=leave_id).update(status="APPROVED")
                        LeaveApplication.objects.filter(id=leave_id).update(status_update_by=obj_emp.name)
                        LeaveApplication.objects.filter(id=leave_id).update(status_update_on=datetime.now())
                        LeaveApplication.objects.filter(id=leave_id).update(category="PAID")
                        LeaveApplication.objects.filter(id=leave_id).update(manager_remarks=manager_remarks)

                        LeaveApplicationDetails.objects.filter(transid=leave_id).update(status="APPROVED")
                        context['save_message'] = 'Leave Request has been approved !!!'
                        # --- sending email to manager -------------
                        to = obj_emp.email
                        rpt_mgr_name = obj_emp.name.split(" ")[0]
                        subject = f'#Leave ID #{leave_id} for {leave_app.leave_type} Leave - approved'
                        html_content = f"Dear {rpt_mgr_name}, <br><p>You have approved the leave request for {leave_app.leave_type} Leave from <strong> {leave_app.leave_start} </strong> to <strong> {leave_app.leave_end} </strong> applied by {obj_user.name}."
                        email_notification(to, subject, html_content)
                        # -------------------------------------------
                        # --- sending email to user -----------------
                        subject = f'Notification: Leave ID #{leave_id} for {leave_app.leave_type} Leave - Approved'
                        to = obj_user.email
                        fname = leave_app.name.split(" ")[0]
                        html_content = f"Dear { fname }, <br> Congratulation, Your Leave Request for {leave_app.leave_type} Leave from <strong> {leave_app.leave_start} </strong> to <strong> {leave_app.leave_end} </strong> has been approved."
                        email_notification(to, subject, html_content)

                        context['form'] = ManagerActionForm(request.POST)
                        return render(request, 'teamleave_view.html', context)
                elif leave_app.unpaid_leave >= 1:
                    leave_details = LeaveApplicationDetails.objects.filter(transid=leave_id)[0]
                    if category == 'UNPAID':

                        lop_obj = LOPRegister(empid=leave_app.empid, name=leave_app.name,
                                              company=leave_app.company, leave_month=leave_details.leave_month,
                                              lop=leave_app.unpaid_leave,
                                              leaveid=leave_id, leave_status=new_status)
                        lop_obj.save()
                    else:
                        pass

                    LeaveApplication.objects.filter(id=leave_id).update(status="APPROVED")
                    LeaveApplication.objects.filter(id=leave_id).update(status_update_by=obj_emp.name)
                    LeaveApplication.objects.filter(id=leave_id).update(status_update_on=datetime.now())
                    LeaveApplication.objects.filter(id=leave_id).update(category=category)
                    LeaveApplication.objects.filter(id=leave_id).update(manager_remarks=manager_remarks)

                    LeaveApplicationDetails.objects.filter(transid=leave_id).update(status="APPROVED")

                    context['save_message'] = f'Leave Request has been approved under {category} category !!!'
                    # --- sending email to manager -------------
                    to = obj_emp.email
                    rpt_mgr_name = obj_emp.name.split(" ")[0]
                    subject = f'#Leave ID #{leave_id} for {leave_app.leave_type} Leave - approved by - {obj_emp.name}'
                    html_content = f"Dear {rpt_mgr_name}, <br><p>You have approved the leave request for {leave_app.leave_type} Leave from <strong> {leave_app.leave_start} </strong> to <strong> {leave_app.leave_end} </strong> applied by {obj_user.name} under <strong> {category} </strong> Leave category."
                    email_notification(to, subject, html_content)
                    # -------------------------------------------
                    # --- sending email to user -----------------
                    subject = f'Notification: Leave ID #{leave_id} for {leave_app.leave_type} Leave - Approved'
                    to = obj_user.email
                    fname = obj_user.name.split(" ")[0]
                    html_content = f"Dear { fname }, <br> Congratulation, Your Leave Request for {leave_app.leave_type} Leave from <strong> {leave_app.leave_start} </strong> to <strong> {leave_app.leave_end} </strong> has been approved under <strong> {category} </strong> Leave category."
                    email_notification(to, subject, html_content)

                    context['form'] = ManagerActionForm(request.POST)
                    return render(request, 'teamleave_view.html', context)
            else:
                LeaveApplication.objects.filter(id=leave_id).update(status="DECLINED")
                LeaveApplication.objects.filter(id=leave_id).update(status_update_by=obj_emp.name)
                LeaveApplication.objects.filter(id=leave_id).update(status_update_on=datetime.now())
                LeaveApplication.objects.filter(id=leave_id).update(category="NA")
                LeaveApplication.objects.filter(id=leave_id).update(manager_remarks=manager_remarks)

                LeaveApplicationDetails.objects.filter(transid=leave_id).update(status="DECLINED")
                context['save_message'] = 'Leave Request has been declined !!!'

                # ------ Update in leave register after declined -----------
                current_fy = FY.objects.get(set_current='YES')
                current_fy = current_fy.financial_year
                leave_register = LeaveRegister.objects.get(financial_year=current_fy, empid=obj_emp.empid)
                if leave_app.leave_type == "Annual":
                    leave_register.al_availed = (float(leave_register.al_availed) - float(leave_app.paid_leave))
                    leave_register.al_closing_balance = (
                                float(leave_register.al_closing_balance) + float(leave_app.paid_leave))
                elif leave_app.leave_type == "Single Day":
                    leave_register.sdl_availed = (float(leave_register.sdl_availed) - float(leave_app.paid_leave))
                    leave_register.sdl_closing_balance = (
                                float(leave_register.sdl_closing_balance) + float(leave_app.paid_leave))
                else:
                    pass
                leave_register.save()


                # --- sending email to manager -------------
                to = obj_emp.email
                rpt_mgr_name = obj_emp.name.split(" ")[0]
                subject = f'#Leave ID #{leave_id} for {leave_app.leave_type} Leave - declined'
                html_content = f"Dear {rpt_mgr_name}, <br><p>You have declined leave request for {leave_app.leave_type} Leave from <strong> {leave_app.leave_start} </strong> to <strong> {leave_app.leave_end} </strong> applied by {obj_user.name}. <br> Remarks: {manager_remarks}."
                email_notification(to, subject, html_content)
                # -------------------------------------------
                # --- sending email to user -----------------
                subject = f'Notification: Leave ID #{leave_id} for {leave_app.leave_type} Leave - Declined'
                to = obj_user.email
                fname = obj_user.name.split(" ")[0]
                html_content = f"Dear { fname }, <br> Sorry !!!, Your Leave Request for {leave_app.leave_type} Leave from <strong> {leave_app.leave_start} </strong> to <strong> {leave_app.leave_end} </strong> has been declined by {obj_emp.name}. <br> Remarks: {manager_remarks}."
                email_notification(to, subject, html_content)

                context['form'] = ManagerActionForm(request.POST)
                return render(request, 'teamleave_view.html', context)
        else:
            return render(request, 'teamleave_view.html', context)
    return render(request, 'teamleave_view.html', context)


class CreditLeaveGetDetails(View):
    template_name = 'credit_leave_details.html'

    def get(self, request):
        context = {
            'obj_fy': FY.objects.all(),
            'form': LeaveRegisterForm,
        }
        # form = LeaveRegisterForm
        context['form'] = LeaveRegisterForm(request.POST)
        return render(request, self.template_name, context)

    def post(self, request):
        context = {'obj_fy': FY.objects.all()}
        form = LeaveRegisterForm(request.POST)
        fy = request.POST.get('financial_year')
        empid = request.POST.get('empid').strip()
        check_emp_count = int(EmployeeDetails.objects.filter(empid=empid).count())
        try:
            if check_emp_count <= 0:
                context['error_msg'] = 'EMPLOYEE ID NOT AVAILABLE !!!'
                context['form'] = LeaveRegisterForm(request.POST)
                return render(request, self.template_name, context)
            else:
                obj_emp = EmployeeDetails.objects.get(empid=empid)
                context['obj_employee_details'] = obj_emp
                emp_doj = obj_emp.date_of_joining
                context['tenure_month'] = (datetime.today().year - emp_doj.year) * 12 + datetime.today().month - emp_doj.month
                current_fy = FY.objects.get(set_current='YES')
                context['current_fy'] = current_fy.financial_year
                # print(fy)
                leave_register = LeaveRegister.objects.get(financial_year=fy, empid=empid)
                context['leave_register'] = leave_register

                # if LeaveRegister.objects.get(financial_year=fy, empid=empid).count() <= 0:
                #     context['obj_leave_annual'] = 0
                # else:
                #     leave_annual = LeaveRegister.objects.get(financial_year=fy, empid=empid, leave_type='Annual')
                #     context['obj_leave_annual'] = leave_annual.closing_balance
                #
                # if LeaveRegister.objects.filter(financial_year=fy, empid=empid, leave_type='Single Day').count() <= 0:
                #     context['obj_leave_single'] = 0
                # else:
                #     leave_single = LeaveRegister.objects.get(financial_year=fy, empid=empid, leave_type='Single Day')
                #     context['obj_leave_single'] = leave_single.closing_balance

                context['form'] = LeaveRegisterForm()
                return render(request, self.template_name, context)
        except Exception as e:
            context['form'] = LeaveRegisterForm(request.POST)
            return render(request, self.template_name, context)


class CreditLeaveSave(View):
    template_name = 'credit_leave_details.html'

    def get(self, request):
        context = {
            'form': LeaveRegisterForm,
            'obj_fy': FY.objects.all()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {
            'form': LeaveRegisterForm,
            'obj_fy': FY.objects.all()
        }
        financial_year = request.POST.get('financial_year')
        empid = request.POST.get('empid')
        name = request.POST.get('name')
        company = request.POST.get('company')
        # leave_type = request.POST.get('leave_type')
        al_opening_balance = float(request.POST.get('al_opening_balance'))
        sdl_opening_balance = float(request.POST.get('sdl_opening_balance'))
        # if opening_balance.isnumeric() :
        #     pass
        # else:
        #     context['error'] = 'Invalid Opening Balance'
        #     ValueError('')
        al_credited = float(request.POST.get('al_credited'))
        sdl_credited = float(request.POST.get('sdl_credited'))
        al_availed = 0
        sdl_availed = 0
        # lop = 0
        al_closing_balance = (al_opening_balance + al_credited) - al_availed
        sdl_closing_balance = (sdl_opening_balance + sdl_credited) - sdl_availed
        # Check if leave already credited
        if LeaveRegister.objects.filter(financial_year=financial_year, empid=empid).count() >= 1:
            context['error_msg'] = 'Already credited for ' + financial_year
            context['form'] = LeaveRegisterForm(request.POST)
            return render(request, self.template_name, context)
        else:
            obj_leave_register = LeaveRegister(financial_year=financial_year,
                                               empid=empid, name=name, company=company,
                                               al_opening_balance=al_opening_balance,
                                               al_credited=al_credited,
                                               al_availed=al_availed,
                                               al_closing_balance=al_closing_balance,
                                               sdl_opening_balance=sdl_opening_balance,
                                               sdl_credited=sdl_credited,
                                               sdl_availed=sdl_availed,
                                               sdl_closing_balance=sdl_closing_balance)

            obj_leave_register.save()
            context['save_message'] = 'Leave credited successfully !!!'
            # --- sending email to user -----------------
            obj_emp = EmployeeDetails.objects.get(empid=empid)
            fname = name.split(" ")[0]
            subject = f'Notification: Leave Credited'
            to = obj_emp.email
            html_content = f"Dear {fname}, <br> Leave has been credited. <br> Single Day: {sdl_credited} <br> Annual Leave: {al_credited}"
            email_notification(to, subject, html_content)

            context['form'] = LeaveRegisterForm(request.POST)
            return render(request, self.template_name, context)


def my_team_view(request):
    context = {}
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    context['obj_my_teams'] = EmployeeDetails.objects.filter(reporting_manager_empid=obj_emp.empid)
    return render(request, 'myteams.html', context)


'''
def credit_leave_get_details_view(request):
    form = LeaveRegisterForm
    context = {
        'obj_fy': FY.objects.all(),
    }
    if request.method == 'POST':
        context['form'] = LeaveRegisterForm(request.POST)
        if form.is_valid:
            try:
                context['form'] = LeaveRegisterForm(request.POST)
                fy = request.POST.get('financial_year')
                # leave_type = request.POST.get('leave_type')
                empid = request.POST.get('empid').strip()
                obj_emp = EmployeeDetails.objects.get(empid=empid)
                context['obj_employee_details'] = obj_emp
                emp_doj = obj_emp.date_of_joining
                context['tenure_month'] = (datetime.today().year - emp_doj.year) * 12 + datetime.today().month - emp_doj.month

                # current_fy = FY.objects.get(set_current='YES')
                context['current_fy'] = fy

                leave_annual = LeaveRegister.objects.get(financial_year=fy, empid=empid, leave_type='Annual')

                context['obj_leave_annual'] = leave_annual.closing_balance

                leave_single = LeaveRegister.objects.get(financial_year=fy, empid=empid, leave_type='Single Day')

                context['obj_leave_single'] = leave_single.closing_balance
                context['form'] = LeaveRegisterForm(request.POST)
                return render(request, 'credit_leave_details.html', context)
            except Exception as e:
                pass
        return render(request, 'credit_leave_details.html', context)
    return render(request, 'credit_leave_details.html', context)

'''

'''
def credit_leave_view(request):
    context = {
        'form': LeaveRegisterForm,
        'obj_fy': FY.objects.all(),
    }
    if request.method == 'POST':
        form = LeaveRegisterForm(request.POST)
        return render(request, 'credit_leave.html', context)
    return render(request, 'credit_leave.html', context)

'''


def my_leave(request):
    context = {}
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    context['obj_leaves_app'] = LeaveApplication.objects.filter(empid=obj_emp.empid).order_by('-applied_on')
    return render(request, 'myleave.html', context)


def team_leave(request):
    context = {}
    obj_emp = EmployeeDetails.objects.get(email=request.user.email)
    context['obj_leaves_app'] = LeaveApplication.objects.filter(reporting_manager_empid=obj_emp.empid).order_by('-applied_on')
    return render(request, 'teamleave.html', context)


def news_view(request):
    context = {}
    return render(request, 'news.html', context)
