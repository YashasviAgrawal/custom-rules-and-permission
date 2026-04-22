from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import User, AdminProfile, DoctorProfile, PatientProfile, StaffProfile, Appointment


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices = User.ROLES_CHOICES)
    admin_code = serializers.CharField(allow_blank=True, required = False)
    license_no = serializers.CharField(allow_blank=True, required = False)
    specialization = serializers.CharField(allow_blank=True, required = False)
    hospital_name = serializers.CharField(allow_blank=True, required = False)
    insurance_no = serializers.CharField(allow_blank=True, required = False)
    medical_history = serializers.CharField(allow_blank=True, required = False)
    employee_id = serializers.CharField(allow_blank=True, required = False)
    department = serializers.CharField(allow_blank=True, required = False)
    doctor = serializers.PrimaryKeyRelatedField(queryset = DoctorProfile.objects.all(), required = False)
    class Meta:
        model = User
        fields = "__all__"
    def validate(self, attrs):
        role = attrs.get('role')
        if role == 'admin' and not attrs.get('admin_code'):
            raise serializers.ValidationError("Admin code is required")
        if role == 'doctor' and not all([attrs.get('license_no'), attrs.get('specialization'), attrs.get('hospital_name')]):
            raise serializers.ValidationError("License number, Specialization and Hospital name are required")
        if role == 'patient' and not attrs.get('insurance_no'):
            raise serializers.ValidationError("Insurance number is required")
        if role == 'staff' and not all([attrs.get('employee_id'), attrs.get('department'), attrs.get('doctor')]):
            raise serializers.ValidationError("Employee ID, Department and Doctor are required")
        return attrs
    def create(self, validated_data):
        role = validated_data.pop('role')
        profile_data = {
            'admin_code': validated_data.pop('admin_code', ''),
            'license_no': validated_data.pop('license_no', ''),
            'specialization': validated_data.pop('specialization', ''),
            'hospital_name': validated_data.pop('hospital_name', ''),
            'insurance_no': validated_data.pop('insurance_no', ''),
            'medical_history': validated_data.pop('medical_history', ''),
            'employee_id': validated_data.pop('employee_id', ''),
            'department': validated_data.pop('department', ''),
            'doctor': validated_data.pop('doctor', None),
        }
        user = User.objects.create_user(**validated_data, role = role)
        if role == 'admin':
            AdminProfile.objects.create(user = user, admin_code = profile_data['admin_code'])
        elif role == 'doctor':
            DoctorProfile.objects.create(user = user, license_no = profile_data['license_no'], specialization = profile_data['specialization'], hospital_name = profile_data['hospital_name'])
        elif role == 'patient':
            PatientProfile.objects.create(user = user, insurance_no = profile_data['insurance_no'], medical_history = profile_data['medical_history'])
        elif role == 'staff':
            StaffProfile.objects.create(user = user, doctor = profile_data['doctor'], employee_id = profile_data['employee_id'], department = profile_data['department'])
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
#         extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role == 'admin':
            data['profile'] = AdminProfile.objects.filter(user = instance).values().first()
        elif instance.role == 'doctor':
            data['profile'] = DoctorProfile.objects.filter(user = instance).values().first()
        elif instance.role == 'patient':
            data['profile'] = PatientProfile.objects.filter(user = instance).values().first()
        elif instance.role == 'staff':
            data['profile'] = StaffProfile.objects.filter(user = instance).values().first()
        return data
# class AdminProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdminProfile
#         fields = ['id', 'user', 'admin_code']

# class DoctorProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DoctorProfile
#         fields = ['id', 'user', 'license_no', 'specialization', 'hospital_name']

# class PatientProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientProfile
#         fields = ['id', 'user', 'insurance_no', 'medical_history']

class StaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(write_only = True)
    email = serializers.EmailField(required = True)
    employee_id = serializers.CharField(required = True)
    department = serializers.CharField(required = True)
    doctor = serializers.PrimaryKeyRelatedField(queryset = DoctorProfile.objects.all(), required = True)
    role = serializers.CharField(default = 'staff')
    permissions = serializers.PrimaryKeyRelatedField(queryset = Permission.objects.all(), many = True, required = True)
    class Meta:
        model = User
        fields = "__all__"
    def create(self, validated_data):
        role = validated_data.pop('role')
        permissions = validated_data.pop('permissions')
        profile_data = {
            'employee_id': validated_data.pop('employee_id', ''),
            'department': validated_data.pop('department', ''),
            'doctor': validated_data.pop('doctor'),
        }
        user = User.objects.create_user(**validated_data, role = role)
        if permissions:
            user.user_permissions.set(permissions)
        StaffProfile.objects.create(user = user, doctor = profile_data['doctor'], employee_id = profile_data['employee_id'], department = profile_data['department'])
        return user

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']
class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many = True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


# class AppointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = ['id', 'patient', 'doctor', 'appointment_time', 'appointment_status', 'remarks', 'appointment_number']