from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from rest_framework import generics
from .models import ( HotelCustomerQuery,
                     HotelEnglishSpeakingCustomerQuery, HotelSpanishSpeakingCustomerQuery,
                     HotelCustomerVoiceCall, HotelInRoomRequest)
from .serializers import (HotelCustomerQuerySerializer,
                          HotelEnglishSpeakingCustomerQuerySerializer, HotelInRoomRequestSerializer,
                          HotelSpanishSpeakingCustomerQuerySerializer,
                          HotelCustomerVoiceCallSerializer, CreateUserSerializer)
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import custom_email_sender, custom_sms_sender, send_email_with_html_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .models import CustomUser as User


## Laundry Clinic View logic

## API View for sending Apology Email to customer for Laundry Clinic

def home(request):
    return render(request, 'reminder/home.html')

class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        messages.success(self.request, "User created successfully!")
        return user


class CreateLaundryClinicEmailApology(generics.CreateAPIView):
    queryset = HotelCustomerQuery.objects.all()
    serializer_class = HotelCustomerQuerySerializer

    def perform_create(self, serializer):
        customer = serializer.save()

        email_sender = 'Laundry Clinic'
        email_subject = 'Follow up on service complaints.'
        email_message = customer.ai_email_response
        email_recipient = customer.email_address

        custom_email_sender(email_recipient, email_subject, email_message, email_sender)

        # determine cusomer language for SMS:
        if customer.language_mode == "English":
            english_sms_message = f"Dear {customer.first_name}, your complaint has been passed to one of our team members to deal with and an email acknowledgement has also been sent to you. We will contact you shortly with a resolution. Thank you for choosing Laundry Clinic."
            custom_sms_sender('Laundry Clinic', customer.phone_number, english_sms_message)
        else:
            spanish_sms_message = f"Estimado {customer.first_name}, su queja se pasó a uno de los miembros de nuestro equipo para que la trate y también se le envió un acuse de recibo por correo electrónico. Nos comunicaremos con usted en breve con una resolución. Gracias por elegir Laundry Clinic."
            custom_sms_sender('Laundry Clinic', customer.phone_number, spanish_sms_message)
            


class CreateLaundryClinicVoiceCall(generics.CreateAPIView):
    queryset = HotelCustomerVoiceCall.objects.all()
    serializer_class = HotelCustomerVoiceCallSerializer



class CreateEnglishSpeakingCustomersQuery(generics.CreateAPIView):
    queryset = HotelEnglishSpeakingCustomerQuery.objects.all()
    serializer_class = HotelEnglishSpeakingCustomerQuerySerializer



class CreateSpanishSpeakingCustomersQuery(generics.CreateAPIView):
    queryset = HotelSpanishSpeakingCustomerQuery.objects.all()
    serializer_class = HotelSpanishSpeakingCustomerQuerySerializer


class UpdateSpanishSpeakingcustomersQuery(generics.RetrieveUpdateAPIView):
    queryset = HotelSpanishSpeakingCustomerQuery.objects.all()
    serializer_class = HotelSpanishSpeakingCustomerQuerySerializer
    lookup_field = 'spreadsheet_row'

class CreateInRoomRequest(generics.CreateAPIView):
    queryset = HotelInRoomRequest.objects.all()
    serializer_class = HotelInRoomRequestSerializer


def list_english_customers(request):
    customers = HotelEnglishSpeakingCustomerQuery.objects.all()

    context = {'customers': customers}
    return render(request, 'reminder/english-customer.html', context)


def list_spanish_customers(request):
    customers = HotelSpanishSpeakingCustomerQuery.objects.all()

    context = {'customers': customers}
    return render(request, 'reminder/spanish-customer.html', context)


@login_required(login_url='login-user')
def laundry_clinic_dashboard_test(request):
    spanish_customers = HotelSpanishSpeakingCustomerQuery.objects.all().order_by(
        '-timestamp', 'status'
    ).values(
        'id',
        'first_name',
        'last_name',
        'email_address',
        'phone_number',
        'customer_query_message_english',
        'location',
        'status',
        'timestamp',
    )

    english_customers = HotelEnglishSpeakingCustomerQuery.objects.all().order_by(
        '-timestamp', 'status'
    ).values(
        'id',
        'first_name',
        'last_name',
        'email_address',
        'phone_number',
        'customer_query_message',
        'location',
        'status',
        'timestamp',
    )

    customer_objs = list(english_customers) + list(spanish_customers)


    paginator = Paginator(customer_objs, 10)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)

    context = {'customers': customers, 'spanish_customers': spanish_customers}

    return render(request, 'reminder/laundry-index.html', context)


@login_required(login_url='login-user')
def get_detail_laundry_clinic_record(request, type, id):
    if type == 'spanish':
        customer = get_object_or_404(HotelSpanishSpeakingCustomerQuery, id=id)
    elif type == 'english':
        customer = get_object_or_404(HotelEnglishSpeakingCustomerQuery, id=id)
    else:
        return HttpResponse("Not Found")

    context = {'customer': customer, 'type': type}
    return render(request, 'reminder/record-detail.html', context)


@login_required(login_url='login-user')
def update_query_status(request, type, id, action_type):
    if type == 'spanish':
        customer = get_object_or_404(HotelSpanishSpeakingCustomerQuery, id=id)
    elif type == 'english':
        customer = get_object_or_404(HotelEnglishSpeakingCustomerQuery, id=id)
    else:
        return HttpResponse("Not Found")
    
    if action_type == 'do':
            customer.status = "Resolved"
    elif action_type == 'undo':
            customer.status = "Open"
    else:
         return HttpResponse("Error: invalid action type")

    customer.save()

    return redirect('laundry-index')

@login_required(login_url='login-user')
def get_all_laundry_clinic_calls(request):
    customer_objs =  HotelCustomerVoiceCall.objects.all()

    paginator = Paginator(customer_objs, 10)
    page_number = request.GET.get('page')
    customer_calls = paginator.get_page(page_number)

    context = {
        'customer_calls': customer_calls,
    }

    return render(request, 'reminder/laundry-clinic-calls.html', context)

@login_required(login_url='login-user')
def get_laundry_clinic_ai_call_detail(request, id):
    customer_call = get_object_or_404(HotelCustomerVoiceCall, id=id)

    context = {
        'customer_call': customer_call,
    }

    return render(request, 'reminder/ai-call-record-detail.html', context)


def login_user(request):
    if request.method == "POST":
        password = request.POST.get('password')
        username = request.POST.get('username')
        
        username_attempt = None
        # Query database to check if username exists
        try:
            username_attempt = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid Username entered")
            # return redirect(reverse(login_user))

        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect('laundry-index')
        else:
            messages.error(request, "Incorrect password")
            return redirect('login-user')
    
    context = {'title': 'Login user'}
    return render(request, 'reminder/login.html', context)


@login_required(login_url='login-user')
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out successfully!")
    return redirect('login-user')


def list_hotel_in_room_requests(request):
    in_room_requests = HotelInRoomRequest.objects.all().order_by('-timestamp')

    paginator = Paginator(in_room_requests, 10)
    page_number = request.GET.get('page')
    guest_requests = paginator.get_page(page_number)

    context = {'guests': guest_requests}
    return render(request, 'reminder/in-room-requests.html', context)
