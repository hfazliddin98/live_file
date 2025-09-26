from django import template
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import re

register = template.Library()

@register.filter
def highlight_mentions(text):
    """@username ko'rinishidagi mention larni highlight qiladi"""
    if not text:
        return text
    
    def replace_mention(match):
        username = match.group(1)
        try:
            user = User.objects.get(username=username)
            return f'<span style="color: #67a3ff; font-weight: 600; background: rgba(103, 163, 255, 0.1); padding: 2px 6px; border-radius: 12px;">@{username}</span>'
        except User.DoesNotExist:
            return f'@{username}'
    
    # @username pattern ni topib, highlight qilish
    highlighted_text = re.sub(r'@(\w+)', replace_mention, text)
    return mark_safe(highlighted_text)

@register.filter
def format_message(text):
    """Matnni format qiladi: mention, link, bold kabi"""
    if not text:
        return text
    
    # Mention larni highlight qilish
    text = highlight_mentions(text)
    
    # URL larni link qilish
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    text = re.sub(url_pattern, lambda m: f'<a href="{m.group()}" target="_blank" style="color: #67a3ff; text-decoration: underline;">{m.group()}</a>', text)
    
    # **bold** matnni qalin qilish
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # *italic* matnni qiyshiq qilish  
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # `code` matnni kod sifatida format qilish
    text = re.sub(r'`(.*?)`', r'<code style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; font-family: monospace;">\1</code>', text)
    
    # Yangi qatorlarni <br> ga o'tkazish
    text = text.replace('\n', '<br>')
    
    return mark_safe(text)

@register.simple_tag
def get_room_members(room):
    """Xona a'zolarini olish"""
    return User.objects.filter(roommember__room=room).distinct()