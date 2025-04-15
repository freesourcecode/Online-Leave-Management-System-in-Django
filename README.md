# Online Leave Management System Project in Django with Source Code

The **Online Leave Management System in Django** created based on **Python**, **Django**, and **SQLITE3 Database**.

The **Online Leave Management System** is a simple project to submit their leave requests electronically.

Through this feature, the employee would be able to restrict the application based on their annual leave credits, which ensures that each employee’s leave credits will be refreshed every year, and the estimates of expended leave credits will be done manually.

An **Online leave management system** contains a list of employees, along with their department and role.

Using this list, the administrator will control the employees who can accept or deny applications. Employees with the title of Principal, Department Director, or Manager have the authority to accept or deny a job application.

This **Online Leave Management System in Django** is an easy project for beginners to learn how to build a web-based python Django project.

>[!NOTE]
> To start creating a Online Leave Management System in Python Django, makes sure that you have PyCharm Professional IDE Installed in your computer.

## Admin Features

* **Dashboard**

For the admin dashboard, you will be able to all the basic access in the whole system. Such as holiday lists, leave application, leave balance, leave category, leave types, company, users, employees.

* **Holiday Lists**

This is the page that lists of all holidays added.

* **Manage Company**

The page where the admin can add, edit and delete company information.

* **Leave Type**

This page lists and manages all forms of leave that the company offers to its employees.

* **Manage Employee**

The admin can manage the employee account. Admin can add, update and Block employee in the system.

*  **Login and Logout**

By default one of the security features of this system is the secure login and logout system.

*  **Leave Applications Page**

This is the page where all of the employees’ leave applications are identified, but only the administrator has access to it.

## Employee Features

* **Login Page**

Employee enter their website credentials on this page to gain access in order to log in.

* **Register Page**

The page where new employee created their login credentials for the website.

* **Home Page**

When customer visit the website, this is the system’s default page.

* **Leave Application**

Only the Principal, Department Head, Manager, and Supervisor have access to this page. 

This is the page where they can accept or reject an employee’s application who works for them.

* **My Application**

This is the page where you can see and track the employee’s leave application.

## How to Create an Online Leave Management System in Django?

Here are the steps on **how to create a Online Leave Management System in Django with Source Code**.

1. **Open file**.

First, open “pycharm professional” after that click “file” and click “new project”.

2. **Choose Django**.

Next, after click “new project”, choose “Django” and click.

3. **Select file location**.

Then, select a file location wherever you want.

4. **Create application name**.

After that, name your application.

5. **Click create**.

Lastly, finish creating project by clicking “create” button.

6.** Start Coding**.

Finally, we will now start adding functionality to our Django Framework by adding some functional codes.

## Functionality and Codes

* Create template for the apply leave form

In this section, we will learn on how create a templates for the apply leave form. To start with, add the following code in your applyleave.html under the folder of applyleave/templates/.

```
{% extends 'base.html' %}
{% load static %}
{% block title %} Leave Request {% endblock %}
{% block heading %} APPLY FOR LEAVE {% endblock %}

{% block content %}

<form method="post" action="{% url 'applyleave' %}" autocomplete="off" style="max-width: 70%;" id="myForm">
    {% csrf_token %}
    <div class="card">
        <div class="card-header" style="background-color:transparent">LEAVE APPLICATION</div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-3 mb-2">
                    <span class="input-text">Leave Type</span>
                    {{ form.leave_type }}
                    <span style="color:red">{{ form.leave_type.errors|striptags }}</span>
                </div>
                <div class="col-md-3 mb-2">
                    <span class="input-text">From</span>
                    {{ form.leave_start }}
                    <span style="color:red">{{ form.leave_start.errors|striptags }}</span>
                </div>
                <div class="col-md-3 mb-3">
                    <span class="input-text">To</span>
                    {{ form.leave_end }}
                    <span style="color:red">{{ form.leave_end.errors|striptags }}</span>
                </div>
                <div class="col-md-3 mb-3">
                    <span class="input-text">Leave For</span>
                    {{ form.leave_for }}
                    <span style="color:red">{{ form.leave_for.errors|striptags }}</span>
                </div>
            </div>
            <div class="row">
                <div class="col-md-3 mb-3" hidden>
                    <span class="input-text">Days</span>
                    {{ form.days }}
                    <span style="color:red">{{ form.days.errors|striptags }}</span>
                </div>
                <div class="col-md-4 mb-3">
                    <span class="input-text">Leave Reason</span>
                    {{ form.reason }}
                    <span style="color:red">{{ form.reason.errors|striptags }}</span>
                </div>
                <div class="col-md-8 mb-3">
                    <span class="input-text">Comments</span>
                    {{ form.comments }}
                    <span style="color:red">{{ form.comments.errors|striptags }}</span>
                </div>
            </div>
            <!--<a href="{% url 'applyleave' %}" role="button" class="btn  btn-primary">Next</a>-->
            <center>
            <button type="submit" class="btn btn-primary" id="btn_leave_app_next" data-toggle="modal"
                    data-target="#applyleave_step2" data-whatever="@mdo">Next
            </button>
            </center>

            {% if save_message %}
            <h5><span class="badge" style="color:Green">{{ save_message }}</span></h5>
            {% else %}
            <h5><span class="badge" style="color:Red">{{ error_message }}</span></h5>
            {% endif %}
        </div>
    </div>
</form>

{% if error_message %}
{% else %}
<form action="{% url 'leave_app_review' %}" method="post" style="max-width: 100%;" id="leave_app_review_form">
    {% csrf_token %}
    <div class="modal fade bd-example-modal-lg" id="myModal" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">APPLY FOR LEAVE - Check for Full Day / Half Day</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">


                    <div class="card">
                        <!--<div class="card-header" style="background-color:transparent">LEAVE APPLICATION DATE WISE BREAKUP</div>-->
                        <div class="card-body">


                            <!--<hr style="border-color:Blue">-->
                            <div class="row" hidden>
                                {{ form }}
                            </div>
                            <!--<div class="alert alert-primary">-->
                            <div class="form-row">
                                <div class="input-group col-md-12 md-2">
                                    <div class="col-md-3 mb-1">
                                        <strong>LEAVE DATE</strong>
                                    </div>
                                    <div class="col-md-3 mb-1">
                                        <strong>DAY</strong>
                                    </div>
                                    <div class="col-md-3 mb-1">
                                        <strong>REMARKS</strong>
                                    </div>
                                    <div class="col-md-3 mb-1">
                                        <strong>LEAVE FOR</strong>
                                    </div>
                                </div>

                            </div>
                            <!--</div>-->
                            <!-- Below loop for populate date wise leaves  -->
                            <!--<div class="alert alert-primary">-->

                            <div class="form-row">
                                {% for key,value in obj_leave_date_list.items %}
                                <div class="input-group col-md-12 mb-2">
                                    <div class="col-md-3 mb-2">
                                        <input type="text" class="form-control"
                                               name="leave_start_{{ key|date:'Y-m-d' }}"
                                               value="{{ key|date:'Y-m-d' }}" readonly>
                                        <!-- obj_leave_app.leave_start|date:'d-M-Y' -->
                                    </div>
                                    <div class="col-md-3 mb-2">
                                        <input class="form-control" id="day" name="day_{{ key|date:'Y-m-d' }}"
                                               value="{{ key|date:'l' }}"
                                               readonly>
                                    </div>

                                    <div class="col-md-3 mb-2">
                                        <input class="form-control" id="remarks" name="remarks_{{ key|date:'Y-m-d' }}"
                                               value="{{ value.remarks }}" readonly>
                                    </div>

                                    <div class="col-md-3 mb-2">
                                        {% if value.remarks == 'Holiday' or value.remarks == 'Weekend' %}
                                        <input type="text" class="form-control" name="leave_for_{{ key|date:'Y-m-d' }}"
                                               value="Full Day" readonly/>
                                        {% else %}
                                        <select class="form-control" name="leave_for_{{ key|date:'Y-m-d' }}">
                                            {% if value.leave_for == 'Full Day' %}
                                            <option value="{{ value.leave_for }}" selected>{{ value.leave_for }}
                                            </option>
                                            <option value="First Half">First Half</option>
                                            <option value="Second Half">Second Half</option>
                                            {% elif value.leave_for == 'First Half' %}
                                            <option value="{{ value.leave_for }}" selected>{{ value.leave_for }}
                                            </option>
                                            <option value="Full Day">Full Day</option>
                                            <option value="Second Half">Second Half</option>
                                            {% elif value.leave_for == 'Second Half' %}
                                            <option value="{{ value.leave_for }}" selected>{{ value.leave_for }}
                                            </option>
                                            <option value="Full Day">Full Day</option>
                                            <option value="First Half">First Half</option>
                                            {% else %}
                                            <option value="Full Day" selected>Full Day</option>
                                            <option value="First Half">First Half</option>
                                            <option value="Second Half">Second Half</option>
                                            {% endif %}
                                        </select>
                                        {% endif %}
                                    </div>
                                </div>
                                {% endfor %}
                            </div>

                            <!--<button class="btn btn-primary" type="submit">Next</button>-->
                            <!--<a href="/applyleave/?from={{ request.path|urlencode }}" role="button" class="btn  btn-primary">Back</a>-->
                            <!--</div>-->
                        </div>
                    </div>


                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Next</button>
                </div>
            </div>
        </div>
    </div>
</form>
{% endif %}


{% if request.method == 'POST' %}
<script>
        $(document).ready(function(){
            $("#myModal").modal('show');
        });

</script>
{% else %}
{% endif %}

<script>
    $(function () {
  $("#datepicker").datepicker({"dateFormat": "yy-mm-dd",
        autoclose: true,
        todayHighlight: true
  }).datepicker('update', new Date());
});

</script>


<script>
     $("#date_start").datepicker({"dateFormat": "yy-mm-dd", beforeShowDay: NotBeforeToday,todayHighlight: true, autoclose: true, todayBtn: true,
        onClose: function () {
            $("#date_end").datepicker(
                "change", {
                minDate: new Date($('#date_start').val())

            });
            myfunc()
            // $("#date_start").datepicker({dateFormat: "yy-mm-dd"});
        }
    });
    $("#date_end").datepicker({"dateFormat": "yy-mm-dd", todayHighlight: true, autoclose: true, todayBtn: true,
        onClose: function () {
            $("#date_start").datepicker(
                "change", {
                // maxDate: new Date($('#date_end').val())
            });
            $("#leave_for").val("Full Day")
            myfunc()
        }
    });

function myfunc(){
    var start= $("#date_start").datepicker("getDate");
    var end= $("#date_end").datepicker("getDate");
    days = (end- start) / (1000 * 60 * 60 * 24);
    // alert(Math.round(days));
    $("#days").val(Math.round(days)+1);
}

function NotBeforeToday(date)
{
    var now = new Date();//this gets the current date and time
    if (date.getFullYear() == now.getFullYear() && date.getMonth() == now.getMonth() && date.getDate() >= now.getDate())
        return [true];
    if (date.getFullYear() >= now.getFullYear() && date.getMonth() > now.getMonth())
       return [true];
     if (date.getFullYear() > now.getFullYear())
       return [true];
    return [false];
}


// $("#leave_for").change(function(){
// if ($("#leave_for").val()=="Full Day"){
// $("#days").val(1);
// }
// else{
// $("#days").val(0.5);
//myfunc();
// }
// });



</script>


<!--<script>-->
<!--$(function(){-->
<!--$("#btn_leave_app_next").click(function(e) {-->
<!--$("#leave_app_form").hide();-->
<!--//$("#btn").hide();-->
<!--});-->
<!--});-->
<!--</script>-->


{% endblock %}
```

* **Create template for the add employee**

In this section, we will learn on how create a templates for the add employee. 

To start with, add the following code in your add_employee.html under the folder of applyleave/templates/.

```
{% extends 'base.html' %}
{% load static %}

{% block title %} Add Employee {% endblock %}

{% block heading %} ADD EMPLOYEE {% endblock %}

{% block content %}


<form action="{% url 'add_employee' %}" method="post" autocomplete="off">
    {% csrf_token %}

    <h2><span class="badge" style="color:Green">{{ save_message }}</span></h2>
            <div class="form-group row">
                {% for field in form %}

                 {% if field.name == 'single_day_entitlement' %}
                    <div class="col-md-3 mb-2">
                        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                        <select class="form-control" id="single_day_entitlement" name="single_day_entitlement">
                         {% for lc in obj_LeaveCategory %}
                          <option name="{{ lc.name }}" value="{{ lc.single_day_entitlement }}">{{ lc.single_day_entitlement }}</option>
                         {% endfor %}
                        </select>
                    </div>

                 {% elif field.name == 'annual_entitlement' %}
                    <div class="col-md-3 mb-2">
                        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                        <select class="form-control" id="annual_entitlement" name="annual_entitlement">
                         {% for lc in obj_LeaveCategory %}
                          <option name="{{ lc.name }}" value="{{ lc.annual_entitlement }}">{{ lc.annual_entitlement }}</option>
                         {% endfor %}
                        </select>
                    </div>
                <!-- Below code for display rest of the field in AddEmployeeForm(ModelForm) -->
                {% else %}
                <div class="col-md-3 mb-2">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                 {{ field }}
                </div>
                {% endif %}
                {% endfor %}
            </div>

                {% if save_message %}
                <a href="{% url 'add_employee' %}" role="button" class="btn btn-primary btn-lg">Close</a>
                {% else %}
                <button class="btn btn-primary btn-lg" type="submit">Save</button>
                {% endif %}

            <div class="form-group row">
                <div class="col-md-12 mb-2">
                <!-- Error Handling -->
                {% if form.errors %}
                {% for field in form %}
                {% for error in field.errors %}
                <div class="alert alert-danger">
                <strong>{{ form.errors|escape }}</strong>
                </div>
                {% endfor %}
                {% endfor %}
                {% for error in form.non_field_errors %}
                <div class="alert alert-danger">
                <strong>{{ error|escape }}</strong>
                </div>
                {% endfor %}
                {% endif %}
                <!-- /Error Handling -->
            </div>
            </div>

</form>


<script>
     $("#date_of_joining").datepicker({"dateFormat": "yy-mm-dd", changeMonth:true, changeYear:true, showButtonPanel:true,todayHighlight: true, autoclose: true, todayBtn: true,
        onClose: function () {
       }
    });
</script>
<script>
    var $leave_category = $( '#leave_category' ),
		$single_day_entitlement = $( '#single_day_entitlement' ),
        $annual_entitlement = $( '#annual_entitlement' ),
        $option1 = $single_day_entitlement.find( 'option' );
        $option2 = $annual_entitlement.find( 'option' );

$leave_category.on( 'change', function() {
	$single_day_entitlement.html( $option1.filter( '[name="' + this.value + '"]' ) );
  $annual_entitlement.html( $option2.filter( '[name="' + this.value + '"]' ) );
} ).trigger( 'change' );
</script>


{% endblock %}
```


* **Create template for the leave balance form**

In this section, we will learn on how create a templates for the leave balance form.

To start with, add the following code in your leave_balance.html under the folder of applyleave/templates/.


```
{% extends 'base.html' %}

{% block title %} Leave Balance {% endblock %}
{% block heading %} LEAVE BALANCE {% endblock %}
{% block content %}

<div class="row">
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">

        <div class="alert alert-primary" role="alert">
            <h5>Annual - Leave Summary</h5>
        </div>

        <!--<p class="card-text">With supporting text below as a natural lead-in to additional content.</p>-->

          <div class="alert alert-success" role="alert">
           {% for bal in leave_register %}
          <h4>Opening Balance <span class="badge badge-primary">{{ bal.al_opening_balance }}</span></h4>
              <hr>
          <h4>Credited <span class="badge badge-primary">{{ bal.al_credited }}</span></h4>
              <hr>
          <h4>Availed <span class="badge badge-info">{{ bal.al_availed }}</span></h4>
              <hr>
          <h4>Available Balance <span class="badge badge-success">{{ bal.al_closing_balance }}</span></h4>
          {% endfor %}
          </div>
        <a href="{% url 'applyleave' %}" class="btn btn-primary">Apply For Leave</a>
      </div>
    </div>
  </div>
  <div class="col-sm-6">
    <div class="card">
      <div class="card-body">

        <div class="alert alert-primary" role="alert">
         <h5>Single Day - Leave Summary</h5>
        </div>

        <!--<p class="card-text">With supporting text below as a natural lead-in to additional content.</p>-->
          <div class="alert alert-success" role="alert">
           {% for bal in leave_register %}
          <h4>Opening Balance <span class="badge badge-primary">{{ bal.sdl_opening_balance }}</span></h4>
              <hr>
          <h4>Credited <span class="badge badge-primary">{{ bal.sdl_credited }}</span></h4>
              <hr>
          <h4>Availed <span class="badge badge-info">{{ bal.sdl_availed }}</span></h4>
              <hr>
          <h4>Available Balance <span class="badge badge-success">{{ bal.sdl_closing_balance }}</span></h4>
          {% endfor %}
          </div>
        <a href="{% url 'applyleave' %}" class="btn btn-primary">Apply For Leave</a>
      </div>
    </div>
  </div>
</div>

{% endblock %}
```


### 📌Here's the full documentation for the [Online Leave Management System Project in Django](https://itsourcecode.com/free-projects/python-projects/online-leave-management-system-project-in-django-with-source-code/)



