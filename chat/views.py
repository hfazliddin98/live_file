from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
import re
from .models import Room, Message, RoomMember


def index(request):
    rooms = Room.objects.all().order_by('-created_at')
    user_count = User.objects.count()
    message_count = Message.objects.count()
    
    context = {
        'rooms': rooms,
        'user_count': user_count,
        'message_count': message_count,
    }
    return render(request, "chat/telegram_index.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat:index')
    
    return render(request, "chat/login.html")





def logout_view(request):
    logout(request)
    return redirect("chat:index")


@login_required
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages_list = Message.objects.filter(room=room).order_by('timestamp')
    
    # Check if user is member of the room
    if not RoomMember.objects.filter(room=room, user=request.user).exists():
        RoomMember.objects.create(room=room, user=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        file = request.FILES.get('file')
        
        if content or file:
            message = Message.objects.create(
                room=room,
                user=request.user,
                content=content,
                file=file
            )
            return redirect('chat:room', room_id=room_id)
    
    context = {
        'room': room,
        'messages': messages_list,
    }
    return render(request, "chat/telegram_room.html", context)


@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        
        if room_name:
            room = Room.objects.create(
                name=room_name,
                created_by=request.user
            )
            # Add creator as member
            RoomMember.objects.create(room=room, user=request.user)
            
            return redirect('chat:room', room_id=room.id)
        else:
            return redirect('chat:create_room')
    
    return render(request, "chat/telegram_create_chat.html")


@login_required
def delete_message_content(request, message_id, content_type):
    """Xabar kontent turini o'chirish: 'text', 'file', 'all'"""
    message = get_object_or_404(Message, id=message_id)
    room = message.room
    
    # Faqat xabar egasi yoki xona yaratuvchisi o'chira oladi
    if request.user != message.user and request.user != room.created_by:
        return redirect('chat:room', room_id=room.id)
    
    if content_type == 'text':
        # Faqat matnni o'chirish
        message.content = ''
        message.save()
    elif content_type == 'file':
        # Faqat faylni o'chirish
        if message.file:
            message.file.delete()  # Faylni diskdan ham o'chirish
            message.file = None
            message.save()
    elif content_type == 'all':
        # Butun xabarni o'chirish
        if message.file:
            message.file.delete()  # Faylni diskdan ham o'chirish
        message.delete()
    
    return redirect('chat:room', room_id=room.id)


@login_required
def get_room_members(request, room_id):
    """Xona a'zolarini JSON formatda qaytarish - autocomplete uchun"""
    room = get_object_or_404(Room, id=room_id)
    
    # Faqat xona a'zolari bu ma'lumotni ko'ra oladi
    if not RoomMember.objects.filter(room=room, user=request.user).exists():
        return JsonResponse({'error': 'Ruxsat yo\'q'}, status=403)
    
    members = []
    for member in RoomMember.objects.filter(room=room).select_related('user'):
        members.append({
            'username': member.user.username,
            'full_name': f"{member.user.first_name} {member.user.last_name}".strip() or member.user.username
        })
    
    return JsonResponse({'members': members})


def upload_file(request):
    return JsonResponse({"success": False})


@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Faqat xona yaratuvchisi o'chira oladi
    if room.created_by != request.user:
        return redirect('chat:room', room_id=room_id)
    
    if request.method == 'POST':
        room_name = room.name
        # Xonadagi barcha fayllarni o'chirish
        for message in room.messages.all():
            if message.file:
                try:
                    message.file.delete()
                except:
                    pass
        
        room.delete()
        return redirect('chat:index')
    
    return redirect('chat:room', room_id=room_id)


@login_required
def delete_message_content(request, message_id, content_type):
    if request.method == 'POST':
        try:
            message = get_object_or_404(Message, id=message_id)
            # Faqat xabar egasi yoki xona admini o'chira oladi
            if message.user == request.user or message.room.created_by == request.user:
                room_id = message.room.id
                
                if content_type == 'text':
                    # Faqat matnni o'chirish
                    message.content = ""
                    message.save()
                    
                elif content_type == 'file':
                    # Faqat faylni o'chirish
                    if message.file:
                        try:
                            message.file.delete()
                        except:
                            pass
                        message.file = None
                        message.file_size = 0
                        message.file_type = None
                        message.save()
                    
                elif content_type == 'all':
                    # Butun xabarni o'chirish
                    if message.file:
                        try:
                            message.file.delete()
                        except:
                            pass
                    message.delete()
                
                return redirect('chat:room', room_id=room_id)
        except:
            pass
    
    return redirect('chat:index')


def delete_file(request, message_id):
    if request.method == 'POST':
        try:
            message = get_object_or_404(Message, id=message_id)
            # Faqat xabar egasi yoki xona admini o'chira oladi
            if message.user == request.user or message.room.created_by == request.user:
                room_id = message.room.id
                if message.file:
                    # Faylni ham o'chirish
                    try:
                        message.file.delete()
                    except:
                        pass
                message.delete()
                return redirect('chat:room', room_id=room_id)
        except:
            pass
    
    return redirect('chat:index')
