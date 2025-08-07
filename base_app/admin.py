from django.contrib import admin
from .models import (
    HotelCustomerQuery,
    HotelEnglishSpeakingCustomerQuery,
    HotelSpanishSpeakingCustomerQuery,
    HotelCustomerVoiceCall,
    CustomUser,
    HotelInRoomRequest

)

# Register your models here.

admin.site.register(HotelCustomerQuery)
admin.site.register(HotelEnglishSpeakingCustomerQuery)
admin.site.register(HotelSpanishSpeakingCustomerQuery)
admin.site.register(HotelCustomerVoiceCall)
admin.site.register(CustomUser)
admin.site.register(HotelInRoomRequest)
