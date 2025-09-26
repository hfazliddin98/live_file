from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    members = models.ManyToManyField(User, through='RoomMember', blank=True, related_name='user_rooms')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    )
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    file_size = models.BigIntegerField(default=0, help_text="Fayl hajmi (bytes)")
    file_type = models.CharField(max_length=100, blank=True, null=True, help_text="MIME type")
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50] if self.content else 'File'}"
    
    def get_file_size_display(self):
        """Fayl hajmini human-readable formatda qaytaradi"""
        if self.file_size == 0:
            return "0 Bytes"
        
        sizes = ['Bytes', 'KB', 'MB', 'GB']
        i = 0
        size = self.file_size
        while size >= 1024 and i < len(sizes) - 1:
            size /= 1024.0
            i += 1
        return f"{size:.1f} {sizes[i]}"
    
    class Meta:
        ordering = ['timestamp']


class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_memberships')
    joined_at = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('room', 'user')
    
    def __str__(self):
        return f"{self.user.username} in {self.room.name}"