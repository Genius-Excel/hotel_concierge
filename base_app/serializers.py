from rest_framework import serializers
from .models import (HotelCustomerQuery, HotelEnglishSpeakingCustomerQuery,
                      HotelSpanishSpeakingCustomerQuery, HotelCustomerVoiceCall, HotelInRoomRequest, CustomUser)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

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


class HotelInRoomRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInRoomRequest
        fields = "__all__"