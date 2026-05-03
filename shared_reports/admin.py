from django.contrib import admin
from .models import SharedReport, ReportMessage

@admin.register(SharedReport)
class SharedReportAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'sender_email', 'doctor', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['sender_name', 'sender_email', 'doctor__name']

@admin.register(ReportMessage)
class ReportMessageAdmin(admin.ModelAdmin):
    list_display = ['report', 'sender_name', 'is_doctor', 'created_at']
