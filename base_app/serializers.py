from rest_framework import serializers
from .models import (HotelCustomerQuery, HotelEnglishSpeakingCustomerQuery,
                      HotelSpanishSpeakingCustomerQuery, HotelCustomerVoiceCall,)


class HotelCustomerQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelCustomerQuery
        fields = "__all__"


class HotelSpanishSpeakingCustomerQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelSpanishSpeakingCustomerQuery
        fields = "__all__"


class HotelEnglishSpeakingCustomerQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelEnglishSpeakingCustomerQuery
        fields = "__all__"


class HotelCustomerVoiceCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelCustomerVoiceCall
        fields = "__all__"
