from django.urls import path
from . import views


urlpatterns = [
     path('add/', views.add_employee_view, name='add_employee'),
     path('all/', views.employee_list_view, name='employee_list'),
     path('<int:id>/details/', views.employee_details_view, name='view_employee'),
     path('<int:id>/edit/', views.employee_edit_view, name='edit_employee'),
     path('<int:id>/delete/', views.employee_delete_view, name='delete_employee'),
     path('profile/', views.profile_view, name='profile_view'),
]
