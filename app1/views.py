from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action 
from .models import User, AdminProfile, DoctorProfile, PatientProfile, StaffProfile, Appointment
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, StaffSerializer, GroupSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor
from django.contrib.auth.models import Group

# Create your views here.

class AuthView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user:
                token = Token.objects.get_or_create(user=user)
                data = UserSerializer(user).data
                data['token'] = token[0].key
                return Response(data, status=status.HTTP_201_CREATED)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]
    def list(self, request):
        doctor = request.user.doctor
        serializer = UserSerializer(doctor.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def get_staff_permissions(self, request):
        group = Group.objects.filter(name='staff')
        if not group:
            return Response({"details": "no permission found"})
        serializer = GroupSerializer(group[0])
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def create_staff(self, request):
        data = request.data.copy()
        data['doctor'] = request.user.doctor.id
        serializer = StaffSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)