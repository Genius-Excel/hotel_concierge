from django.urls import path
from . import views


urlpatterns = [
  # Laundry Clinic PATHS
    #path('', views.home, name='home'),
    path('api/send-customer-apology', views.CreateLaundryClinicEmailApology.as_view(), name='send-customer-apology'),
    path('api/laundry-clinic-voice-call', views.CreateLaundryClinicVoiceCall.as_view(), name='laundry-clinic-voice-call'),
    path('api/create-english-customer-query', views.CreateEnglishSpeakingCustomersQuery.as_view(), name='english-customers'),
    path('api/create-spanish-customer-query', views.CreateSpanishSpeakingCustomersQuery.as_view(), name='spanish-customers'),
    path('api/update-spanish-customer-query/<int:spreadsheet_row>', views.UpdateSpanishSpeakingcustomersQuery.as_view(), name='update-spanish-customers'),

    path('api/create-in-room-request', views.CreateInRoomRequest.as_view(), name='create-in-room-request'),
    
    path('login-user/', views.login_user, name='login-user'),
    path('logout-user/', views.logout_user, name='logout-user'),
    path('list-english-customers/', views.list_english_customers, name='list-english-customers'),
    path('list-spanish-customers/', views.list_spanish_customers, name='list-spanish-customers'),
    path('', views.laundry_clinic_dashboard_test, name='laundry-index'),
    path('laundry-clinic-ai-calls/', views.get_all_laundry_clinic_calls, name='laundry-clinic-calls'),
    path('laundry-clinic-ai-call/detail/<uuid:id>/', views.get_laundry_clinic_ai_call_detail, name='ai-call-detail'),
    path('detail/<str:type>/<uuid:id>', views.get_detail_laundry_clinic_record, name='record-detail'),
    path('update-record-status/<str:type>/<uuid:id>/<str:action_type>/', views.update_query_status, name='update-record-status'),


]