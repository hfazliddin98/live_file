# Live Chat Project

Django asosidagi real-time chat ilovasi fayl saqlash imkoniyati bilan.

## Xususiyatlar
- Real-time messaging (WebSocket)
- **Har qanday fayl yuklash va saqlash** - 50MB gacha, barcha formatlar
- **Yopiq registratsiya** - faqat admin foydalanuvchi yarata oladi
- Chat xonalari
- Responsive design
- Admin panel orqali foydalanuvchi boshqaruvi
- **Xavfsizlik** - xavfli fayllar (.exe, .bat, etc.) taqiqlangan

## O'rnatish

1. Virtual environment yarating:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki Windows uchun: venv\Scripts\activate
```

2. Dependencies o'rnating:
```bash
pip install -r requirements.txt
```

3. Redis server ishga tushiring:
```bash
sudo systemctl start redis-server
```

4. Migration bajaring:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Superuser yarating:
```bash
python manage.py createsuperuser
```

6. Serverni ishga tushiring:
```bash
python manage.py runserver
```

## Foydalanish

### Admin uchun:
1. Admin panel: http://127.0.0.1:8000/admin
2. Yangi foydalanuvchilar yarating
3. Chat xonalari va xabarlarni boshqaring

### Foydalanuvchilar uchun:
1. Asosiy sahifa: http://127.0.0.1:8000
2. Admin tomonidan yaratilgan login bilan kiring
3. Chat xonasiga boring va real-time chat qiling
4. Fayl yuklash uchun fayl tugmasini bosing

## Texnologiyalar
- **Backend:** Django 4.2.7, Django Channels, Redis
- **Frontend:** Bootstrap 5, JavaScript, WebSocket
- **Ma'lumotlar bazasi:** SQLite
- **Real-time:** Django Channels + Redis

## Registratsiya
⚠️ **Registratsiya yopiq** - yangi foydalanuvchilarni faqat admin yarata oladi.