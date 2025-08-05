from django.contrib import admin
from .models import (
    HotelCustomerQuery,
    HotelEnglishSpeakingCustomerQuery,
    HotelSpanishSpeakingCustomerQuery,
    HotelCustomerVoiceCall,

)

# Register your models here.

admin.site.register(HotelCustomerQuery)
admin.site.register(HotelEnglishSpeakingCustomerQuery)
admin.site.register(HotelSpanishSpeakingCustomerQuery)
admin.site.register(HotelCustomerVoiceCall)
