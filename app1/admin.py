from django.contrib import admin
from .models import User, AdminProfile, DoctorProfile, PatientProfile, StaffProfile, Appointment

# Register your models here.
admin.site.register(User)
admin.site.register(AdminProfile)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(StaffProfile)
admin.site.register(Appointment)
