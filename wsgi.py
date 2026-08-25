# wsgi.py
import sys
import os

# Конфигурация для PythonAnywhere
USERNAME = 'bakhtiyorsattaroff'
PROJECT_HOME = f'/home/{USERNAME}/education-platform'
VENV_PATH = f'/home/{USERNAME}/.virtualenvs/my_venv/lib/python3.10/site-packages'

# Добавляем пути
if PROJECT_HOME not in sys.path:
    sys.path.insert(0, PROJECT_HOME)

if VENV_PATH not in sys.path:
    sys.path.insert(0, VENV_PATH)

# Переключаемся в папку проекта
os.chdir(PROJECT_HOME)

# Импортируем приложение
from app import app as application