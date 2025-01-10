# **Tattoo healing bot**

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/)
![SQLite](https://a11ybadges.com/badge?logo=sqlite)

Телеграм бот для сопровождения заживления новой татуировки у клиента. В зависимости от выбора заживления, бот будет несколько раз в день слать определенные инструкции, как ухаживать за тату, пока она не заживет.
Если пользователь удаляет и банит бота, его данные из бд стираются.  
Также создана админ зона - админ может отправлять посты, которые потом будут разосланы всем пользователям.

Стек: aiogram, SQLalchemy, telegram, SQLite, python, apscheduler

### Локальный запуск бота:

**_Склонировать репозиторий к себе_**
```
git clone https://github.com/TatianaSharova/Tattoo_healing-bot.git
```
**_В директории проекта создать файл .env и заполнить своими данными:_**
```
TELEGRAM_TOKEN                          - токен от телеграм бота
ADMIN                                   - телеграм id админа 1
ADMIN_2                                 - телеграм id админа 2
DB                                      - 'sqlite+aiosqlite:///bot_base.db'
```
**_Создать и активировать виртуальное окружение:_**

Для Linux/macOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Для Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
**_Установить зависимости из файла requirements.txt:_**
```
pip install -r requirements.txt
```
**_Запустить бот:_**
Для Linux/macOS:
```
python3 tattoo_bot.py
```
```
source venv/bin/activate
```
Для Windows:
```
python tattoo_bot.py
```

### Автор
[Татьяна Шарова](https://github.com/TatianaSharova)
