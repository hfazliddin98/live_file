#!/bin/bash

# Deploy script for Live Chat
echo "🚀 Live Chat deploy boshlandi..."

# Virtual environment faollashtirish
echo "📦 Virtual environment faollashtirish..."
source venv/bin/activate

# Dependencies o'rnatish
echo "📚 Dependencies o'rnatish..."
pip install -r requirements.txt

# Migration'larni amalga oshirish
echo "🔄 Database migration'lari..."
python manage.py makemigrations
python manage.py migrate

# Static fayllarni yig'ish
echo "📁 Static fayllarni yig'ish..."
python manage.py collectstatic --noinput

# Admin user yaratish
echo "👤 Admin user yaratish..."
python manage.py create_admin --username=admin --password=admin123

# Media papka ruxsatlarini sozlash
echo "📂 Media papka ruxsatlarini sozlash..."
mkdir -p media/chat_files
chmod 755 media
chmod 755 media/chat_files

echo "✅ Deploy muvaffaqiyatli tugadi!"
echo ""
echo "🔐 Login ma'lumotlari:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "🌐 Sayt tayyor!"