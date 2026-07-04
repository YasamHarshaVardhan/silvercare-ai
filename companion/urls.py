from django.urls import path
from . import views

urlpatterns = [
    path('', views.companion_view, name='companion'),
    path('add/', views.add_data_view, name='add_data'),
    path('chat_api/', views.chat_api, name='chat_api'),
    path('check_alerts/', views.check_alerts_api, name='check_alerts'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('manage/', views.manage_records_view, name='manage_records'),
    path('medication/edit/<int:med_id>/', views.update_medication, name='update_medication'),
    path('appointment/edit/<int:app_id>/', views.update_appointment, name='update_appointment'),
    path('medication/delete/<int:med_id>/', views.delete_medication, name='delete_medication'),
    path('appointment/delete/<int:app_id>/', views.delete_appointment, name='delete_appointment'),
]

