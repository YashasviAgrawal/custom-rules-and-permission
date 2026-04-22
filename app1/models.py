from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
# Create your models here.

class User(AbstractUser):
    ROLES_CHOICES = [
        ('admin', 'admin'),
        ('doctor', 'doctor'),
        ('patient', 'patient'),
        ('staff', 'staff'),
    ]
    role = models.CharField(max_length=10, choices=ROLES_CHOICES)

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_user')
    admin_code = models.CharField(max_length=10, unique=True)
    
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    license_no = models.CharField(max_length=100, unique=True)
    specialization = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    insurance_no = models.CharField(max_length=100, unique=True)
    medical_history = models.TextField(null = True, blank = True)

    class Meta:
        permissions = [
            ('view_all_patients', 'Can view all patients'),
            ('edit_patient_records', 'Can edit patient records'),
        ]
    
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='staff')
    employee_id = models.CharField(max_length=100, unique=True)    
    department = models.CharField(max_length=100)   

def generate_number(*args, **kwargs):
        return str(uuid.uuid4()).split('-')[0]
    
class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_time = models.DateTimeField()
    appointment_status = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100, null = True, blank = True) 
    appointment_number = models.CharField(max_length=100, unique=True, default=generate_number)

    class Meta:
        permissions = [
            ('view_all_appointments', 'Can view all appointments'),
            ('create_appointment', 'Can create appointments'),
            ('update_appointment', 'Can update appointments'),
            ('cancel_appointment', 'Can cancel appointments'),
        ]