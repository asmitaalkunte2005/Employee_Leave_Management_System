from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_leave, name='apply_leave'),
    path('display/', views.display_leave, name='display_leave'),
    path('update/<int:id>/', views.update_leave, name='update_leave'),
    path('delete/<int:id>/', views.delete_leave, name='delete_leave'),


    path("api/leaves/", views.leave_list_api),

    path("api/leaves/<int:id>/", views.leave_detail_api),

    path("api/leaves/create/", views.leave_create_api),

    path("api/leaves/update/<int:id>/", views.leave_update_api),

    path("api/leaves/delete/<int:id>/", views.leave_delete_api),
]