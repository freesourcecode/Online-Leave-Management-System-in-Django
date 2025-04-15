from django.urls import path
from . import views
from .views import CreditLeaveGetDetails, CreditLeaveSave, ApplyLeaveView, LeaveAppReview, LeaveAppSubmit

urlpatterns = [
     path('applyleave/', ApplyLeaveView.as_view(), name='applyleave'),
     path('applyleave_review/', LeaveAppReview.as_view(), name='leave_app_review'),
     path('applyleave_submit/', LeaveAppSubmit.as_view(), name='leave_app_submit'),
     # path('applyleave_review/', views.leave_app_review, name='leave_app_review'),
     # path('applyleave', views.applyleave_view, name='applyleave'),
     path('balance/', views.check_leave_balance_view, name='leave_balance'),
     path('holiday_list/', views.holiday_list_view, name='holiday_list'),
     path('latestnews/', views.news_view, name='news'),
     path('credit_leave_details/', CreditLeaveGetDetails.as_view(), name='credit_leave_get_details'),
     path('credit_leave_save/', CreditLeaveSave.as_view(), name='credit_leave_save'),
     path('myleave/', views.my_leave, name='my_leave'),
     path('myleave/<int:id>/view/', views.my_leave_view, name='my_leave_view'),
     path('myleave/<int:id>/cancel/', views.my_leave_cancel, name='my_leave_cancel'),
     path('teamleave/', views.team_leave, name='team_leave'),
     path('teamleave/<int:id>/view/', views.team_leave_view, name='my_leave_view'),
     path('teamleave/action/', views.leave_manager_action, name='team_leave_action'),
     path('myteams/', views.my_team_view, name='my_teams'),
     # path('credit_leave/', views.credit_leave_view, name='credit_leave'),
     # path('credit_leave_details/', views.credit_leave_get_details_view, name='credit_leave_get_details'),
]




