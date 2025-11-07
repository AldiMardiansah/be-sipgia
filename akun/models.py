# akun/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid

class Akun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'akun'  # Nama tabel di database
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash password sebelum disimpan"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Cek password saat login"""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Hash password otomatis kalau belum di-hash
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)