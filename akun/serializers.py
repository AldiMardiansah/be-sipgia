# akun/serializers.py
from rest_framework import serializers
from .models import Akun
import re

class AkunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Akun
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=6,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}, 
        label='Confirm Password'
    )

    class Meta:
        model = Akun
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate_username(self, value):
        """Validasi username"""
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters")
        
        if Akun.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        
        # Validasi karakter
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers and underscore")
        
        return value

    def validate_email(self, value):
        """Validasi email"""
        if Akun.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, attrs):
        """Validasi password match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """Create akun baru"""
        # Hapus password2 karena tidak disimpan
        validated_data.pop('password2')
        
        # Create akun (password akan di-hash otomatis di model)
        akun = Akun.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        
        return akun

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Cek apakah akun ada
        try:
            akun = Akun.objects.get(username=username)
        except Akun.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        # Cek password
        if not akun.check_password(password):
            raise serializers.ValidationError("Invalid username or password")

        # Cek apakah akun aktif
        if not akun.is_active:
            raise serializers.ValidationError("Account is inactive")

        attrs['akun'] = akun
        return attrs