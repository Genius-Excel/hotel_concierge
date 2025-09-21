from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Department(models.Model):
    """Department model for hotel organizational structure"""
    DEPARTMENT_CHOICES = [
        ('ADMIN', 'Hotel Administration'),
        ('KITCHEN', 'Kitchen Department'),
        ('FRONT_DESK', 'Front Desk'),
        ('HOUSEKEEPING', 'Housekeeping'),
        ('LAUNDRY', 'Laundry Services'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']


class Role(models.Model):
    """Role model for granular permissions"""
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Department Manager'),
        ('SUPERVISOR', 'Supervisor'),
        ('STAFF', 'Staff Member'),
        ('VIEWER', 'View Only'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='roles')
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=True)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_manage_staff = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.department.get_name_display()}"
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        unique_together = ['name', 'department']
        ordering = ['department', 'name']


class CustomUser(AbstractUser):
    """Enhanced custom user model for hotel staff"""
    EMPLOYMENT_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('TERMINATED', 'Terminated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='ACTIVE')
    hire_date = models.DateField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')

    def clean(self):
        super().clean()
        if self.role and self.department and self.role.department != self.department:
            raise ValidationError("Role must belong to the same department as the user.")

    def has_permission(self, permission_type):
        """Check if user has specific permission"""
        if self.is_superuser:
            return True
        if not self.role:
            return False
        return getattr(self.role, f'can_{permission_type}', False)

    def can_access_department_data(self, department_name):
        """Check if user can access specific department data"""
        if self.is_superuser:
            return True
        if not self.department:
            return False
        return self.department.name == department_name or self.department.name == 'ADMIN'

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']


# ...existing code... (keep all your existing models)

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
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_queries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


status_options = (
    ("Open", "Open"),
    ("In Progress", "In Progress"),
    ("Resolved", "Resolved"),
    ("Cancelled", "Cancelled"),
)


class HotelEnglishSpeakingCustomerQuery(models.Model):
    """This is the model class of Laundry Clinic English Speakers"""
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
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_english_queries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']


class HotelSpanishSpeakingCustomerQuery(models.Model):
    """This is the model class of Laundry Clinic Spanish Speakers"""
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
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_spanish_queries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']


class HotelCustomerVoiceCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    caller_name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=150, null=True)
    call_summary = models.TextField()
    call_transcript = models.TextField()
    recording_url = models.TextField(null=True)
    handled_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_calls')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class HotelInRoomRequest(models.Model):
    REQUEST_STATUSES = (
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )
    
    REQUEST_TYPES = (
        ("HOUSEKEEPING", "Housekeeping"),
        ("MAINTENANCE", "Maintenance"),
        ("ROOM_SERVICE", "Room Service"),
        ("LAUNDRY", "Laundry"),
        ("CONCIERGE", "Concierge"),
        ("OTHER", "Other"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    room_number = models.CharField(max_length=50, null=True)
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES, null=True)
    request_details = models.TextField()
    request_status = models.CharField(max_length=50, choices=REQUEST_STATUSES, default="Open", null=True)
    priority = models.CharField(max_length=20, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    timestamp = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Request {self.id} - Room {self.room_number}"


class AuditLog(models.Model):
    """Audit log for tracking user actions"""
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, null=True, blank=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']