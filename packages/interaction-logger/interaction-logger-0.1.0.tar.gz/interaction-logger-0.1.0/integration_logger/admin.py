from django.contrib import admin
from .models import UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'method', 'path', 'operation_type', 'response_status')
    list_filter = ('method', 'operation_type', 'response_status', 'timestamp')
    search_fields = ('user__username', 'path', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'path', 'method', 'request_data', 'response_status',
                      'ip_address', 'user_agent', 'operation_type')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
