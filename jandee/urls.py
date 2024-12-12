from django.urls import path
from . import views

urlpatterns = [
    path("", views.submit_report, name="submit_report"),
    path("success/", views.report_success, name="report_success"),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('add_branch/', views.add_branch, name='add_branch'),
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/edit/<int:branch_id>/', views.edit_branch, name='edit_branch'),
    path('branches/delete/<int:branch_id>/', views.delete_branch, name='delete_branch'),
    path('edit_transaction/<int:id>/', views.edit_transaction, name='edit_transaction'), 
    path('view_sms_text/<int:transaction_id>/', views.view_sms_text, name='view_sms_text'),
    path('accounts/logout/', views.custom_logout, name='logout'), 
]
