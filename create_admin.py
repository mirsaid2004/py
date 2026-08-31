# create_admin.py
"""Создание администратора вручную.

Запускать из папки проекта:

    python create_admin.py

Скрипт спрашивает логин и пароль, пароль вводится скрытно и не
сохраняется в истории команд. Пароля по умолчанию больше нет:
учётная запись admin/admin123 была известна всем, кто видел код.
"""
import os
import sys
import getpass

# Этот скрипт не обслуживает запросы и не подписывает cookie, поэтому
# настоящий SECRET_KEY ему не нужен. Ставим заглушку до импорта config,
# иначе ProductionConfig потребует переменную окружения.
os.environ.setdefault('SECRET_KEY', 'cli-script-does-not-sign-cookies')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import JSONStorage, PasswordManager
from services import UserService
from models import User, UserRoles, UserStatus, AccessType


def ask(prompt, required=True, validator=None):
    while True:
        value = input(prompt).strip()
        if not value:
            if required:
                print("   Bu maydon bo'sh bo'lmasligi kerak.\n")
                continue
            return ''
        if validator:
            ok, msg = validator(value)
            if not ok:
                print(f"   {msg}\n")
                continue
        return value


def ask_password():
    print("\nParol talablari: kamida 6 ta belgi, 1 katta harf, "
          "1 kichik harf, 1 raqam.")
    while True:
        pwd = getpass.getpass("Parol (ko'rinmaydi): ")
        ok, errors = PasswordManager.validate_password_strength(pwd)
        if not ok:
            for e in errors:
                print(f"   {e}")
            print()
            continue
        if pwd != getpass.getpass("Parolni takrorlang: "):
            print("   Parollar mos kelmadi.\n")
            continue
        return pwd


def main():
    storage = JSONStorage()
    service = UserService(storage)

    existing = service.get_all_users()
    admins = [u for u in existing if u.get('role') == UserRoles.ADMIN]
    if admins:
        print(f"\nMavjud adminlar ({len(admins)}):")
        for a in admins:
            print(f"  - {a.get('login')}  ({a.get('full_name', '')})")

    print()
    login = ask("Login: ", validator=User.validate_login)

    # Если логин занят, предлагаем сменить пароль. Это нужно, чтобы можно
    # было починить уже созданный admin/admin123 на работающем сайте.
    current = service.get_user_by_login(login)
    if current:
        print(f"\n'{login}' allaqachon mavjud.")
        if input("Uning parolini yangilaysizmi? (ha/yo'q): ").strip().lower() not in ('ha', 'h', 'yes', 'y'):
            print("Bekor qilindi.")
            return 1
        service.change_user_password(current['id'], ask_password())
        print(f"\n[OK] '{login}' uchun parol yangilandi.")
        return 0

    full_name = ask("To'liq ism: ")
    email = ask("Email (ixtiyoriy, Enter - o'tkazish): ",
                required=False, validator=User.validate_email)
    phone = ask("Telefon (ixtiyoriy, Enter - o'tkazish): ",
                required=False, validator=User.validate_phone)
    password = ask_password()

    user = service.create_user({
        'full_name': full_name,
        'login': login,
        'email': email,
        'phone': phone,
        'password': password,
        'role': UserRoles.ADMIN,
        'status': UserStatus.ACTIVE,
        'access_type': AccessType.FREE,
    })
    print(f"\n[OK] Admin yaratildi: {user['login']}")
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nBekor qilindi.")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[XATO] {e}")
        sys.exit(1)
