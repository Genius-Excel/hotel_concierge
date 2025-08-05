from django.db import models
import uuid

language_options = (
    ("English", "English"),
    ("Spanish", "Spanish"),
)

class HotelCustomerQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    customer_query_message = models.TextField()
    ai_email_response = models.TextField()
    phone_number = models.CharField(max_length=50, null=True)
    email_address = models.EmailField()
    language_mode = models.CharField(max_length=50, choices=language_options, default="English", null=True)


status_options = (
    ("Open", "Open"),
    ("Resolved", "Resolved"),
)


class HotelEnglishSpeakingCustomerQuery(models.Model):
    """This is the model class of Laundry Clinic English Speakers
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    customer_query_message = models.TextField()
    customer_comments = models.TextField()
    ai_assistant_response = models.TextField()
    laundry_event_details = models.TextField()
    location = models.CharField(max_length=150)
    timestamp = models.DateTimeField()
    ai_email_response = models.TextField()
    phone_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50, null=True, choices=status_options, default="Open")



class HotelSpanishSpeakingCustomerQuery(models.Model):
    """This is the model class of Laundry Clinic Spanish Speakers
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    spreadsheet_row = models.IntegerField(null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=50, null=True)
    customer_query_message_english = models.TextField(null=True)
    customer_query_message_spanish = models.TextField(null=True)
    customer_comments_english = models.TextField(null=True)
    customer_comments_spanish = models.TextField(null=True)
    ai_assistant_response_english = models.TextField(null=True)
    ai_assistant_response_spanish = models.TextField(null=True)
    laundry_event_details_english = models.TextField(null=True)
    laundry_event_details_spanish = models.TextField(null=True)
    location = models.CharField(max_length=150, null=True)
    timestamp = models.DateTimeField()
    ai_email_response_spanish = models.TextField(null=True)
    status = models.CharField(max_length=50, null=True, choices=status_options, default="Open")


class HotelCustomerVoiceCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    caller_name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=150, null=True)
    call_summary = models.TextField()
    call_transcript = models.TextField()
    recording_url = models.TextField(null=True)


class HotelInRoomRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    customer_name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    room_number = models.CharField(max_length=50, null=True)
    request_type = models.CharField(max_length=50, null=True)
    request_details = models.TextField()
    request_status = models.CharField(max_length=50, choices=status_options, default="Open", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)