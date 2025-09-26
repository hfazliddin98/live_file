from d@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'member_count', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name']
    readonly_fields = ['created_at']contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Room, Message, RoomMember


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'member_count']
    list_filter = ['created_at', 'created_by']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'A\'zolar soni'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'content_preview', 'message_type', 'timestamp']
    list_filter = ['message_type', 'timestamp', 'room']
    search_fields = ['content', 'user__username', 'room__name']
    readonly_fields = ['timestamp', 'file_size', 'file_type']
    
    def content_preview(self, obj):
        if obj.content:
            return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
        return 'Fayl'
    content_preview.short_description = 'Xabar'


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'is_admin', 'joined_at']
    list_filter = ['is_admin', 'joined_at', 'room']
    search_fields = ['user__username', 'room__name']
    readonly_fields = ['joined_at']


# Custom User Admin - foydalanuvchilarni boshqarish uchun
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'room_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def room_count(self, obj):
        return Room.objects.filter(created_by=obj).count()
    room_count.short_description = 'Yaratgan xonalar'

# Admin panelni qayta ro'yxatdan o'tkazish
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin panel sarlavhalarini o'zgartirish
admin.site.site_header = 'Live Chat Admin Panel'
admin.site.site_title = 'Live Chat'
admin.site.index_title = 'Live Chat Boshqaruv Paneli'
