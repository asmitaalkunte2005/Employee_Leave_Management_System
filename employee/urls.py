from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('dashboard/', views.dashboard_view, name='home'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('insert/', views.insert_view, name='insert'),
    path('display/', views.display_view, name='display'),
    path('update/<int:id>/', views.update_view, name='update'),
    path('delete/<int:id>/', views.delete_view, name='delete'),
    path('api/employees/', views.employee_list_api),
    path('api/employees/<int:id>/', views.employee_detail_api),
    path('api/employees/create/', views.employee_create_api),
    path('api/employees/update/<int:id>/', views.employee_update_api),
    path('api/employees/delete/<int:id>/', views.employee_delete_api),
]