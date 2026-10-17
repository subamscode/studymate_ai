from django.contrib import admin
from .models import ChatMessage, ChatSession, StudyDocument
class ChatMessageInline(admin.TabularInline):
    model=ChatMessage; extra=0; readonly_fields=("role", "content", "created_at")
@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display=("id", "title", "user", "created_at", "updated_at"); search_fields=("title", "user__username"); inlines=[ChatMessageInline]
@admin.register(StudyDocument)
class StudyDocumentAdmin(admin.ModelAdmin):
    list_display=("id", "original_name", "user", "status", "chunk_count", "uploaded_at"); list_filter=("status",); search_fields=("original_name", "user__username")
