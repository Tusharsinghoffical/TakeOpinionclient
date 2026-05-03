from django.contrib import admin
from .models import Enquiry, FAQ, ChatMessage


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'status', 'created_at', 'is_resolved']
    list_filter = ['status', 'is_resolved', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['enquiry', 'sender_type', 'timestamp', 'is_read']
    list_filter = ['sender_type', 'is_read', 'timestamp']
    search_fields = ['message', 'enquiry__subject']