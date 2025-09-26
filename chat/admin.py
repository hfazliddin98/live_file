from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Room, Message, RoomMember


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'member_count', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']
    readonly_fields = ['created_at']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'A\'zolar soni'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'user', 'room', 'timestamp', 'has_file']
    list_filter = ['timestamp', 'room']
    search_fields = ['content', 'user__username', 'room__name']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        if obj.content:
            return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
        elif obj.file:
            return f"📎 {obj.file.name}"
        return "Bo'sh xabar"
    content_preview.short_description = 'Xabar'
    
    def has_file(self, obj):
        return bool(obj.file)
    has_file.boolean = True
    has_file.short_description = 'Fayl'


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'joined_at']
    list_filter = ['joined_at', 'room']
    search_fields = ['user__username', 'room__name']


# Custom User Admin
class ChatUserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('room_count',)
    
    def room_count(self, obj):
        return obj.created_rooms.count()
    room_count.short_description = 'Yaratgan xonalar'


# Unregister the original User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, ChatUserAdmin)

# Admin site headers
admin.site.site_header = "Live Chat Admin Panel"
admin.site.site_title = "Live Chat Admin"
admin.site.index_title = "Live Chat Dashboard"