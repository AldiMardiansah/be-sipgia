# akun/admin.py
from django.contrib import admin
from .models import Akun

@admin.register(Akun)
class AkunAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'password']
    
    fieldsets = (
        ('Account Info', {
            'fields': ('id', 'username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Bisa dihapus dari admin
        return True
    
    def has_add_permission(self, request):
        # Tidak bisa tambah dari admin, harus lewat register
        return False