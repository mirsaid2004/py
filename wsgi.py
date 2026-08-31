# wsgi.py
"""Точка входа для WSGI-сервера.

Путь к проекту вычисляется по расположению этого файла, поэтому имя
пользователя и название папки нигде не прописаны.

Внимание: на PythonAnywhere сервер использует НЕ этот файл, а свой,
в /var/www/<username>_pythonanywhere_com_wsgi.py. Там путь нужно
указать явно, потому что тот файл лежит вне папки проекта.
"""
import sys
import os

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

if PROJECT_HOME not in sys.path:
    sys.path.insert(0, PROJECT_HOME)

os.chdir(PROJECT_HOME)

from app import app as application
