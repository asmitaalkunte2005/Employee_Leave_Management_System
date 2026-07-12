from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='home'),

    # path('dashboard/', views.dashboard_view, name='dashboard'),

    path('insert/', views.insert_view, name='insert'),

    path('display/', views.display_view, name='display'),

    path('update/<int:id>/', views.update_view, name='update'),

    path('delete/<int:id>/', views.delete_view, name='delete'),

    path("api/employees/", views.employee_list_api),

    path("api/employees/<int:id>/", views.employee_detail_api),

    path("api/employees/create/", views.employee_create_api),

    path("api/employees/update/<int:id>/", views.employee_update_api),

    path("api/employees/delete/<int:id>/", views.employee_delete_api),
]