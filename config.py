# config.py
import os
from datetime import timedelta


class Config:
    # Базовые настройки
    SECRET_KEY = 'dev-secret-key-change-in-production-2026'
    DEBUG = False  # На сервере всегда False
    TESTING = False

    # Настройки сессий
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # На сервере True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Определяем окружение
    IS_PYTHONANYWHERE = True  # Флаг для сервера
    USERNAME = 'bakhtiyorsattaroff'

    # Пути для PythonAnywhere
    if IS_PYTHONANYWHERE:
        HOME_DIR = f'/home/{USERNAME}'
        BASE_DIR = os.path.join(HOME_DIR, 'education-platform')
    else:
        # Локальная разработка
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Все директории
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    STORAGE_DIR = os.path.join(BASE_DIR, 'storage')
    BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')

    # Поддиректории storage
    VIDEO_DIR = os.path.join(STORAGE_DIR, 'videos')
    DOCUMENTS_DIR = os.path.join(STORAGE_DIR, 'documents')
    IMAGES_DIR = os.path.join(STORAGE_DIR, 'images')
    PRESENTATIONS_DIR = os.path.join(STORAGE_DIR, 'presentations')
    OTHER_DIR = os.path.join(STORAGE_DIR, 'other')
    RECEIPTS_DIR = os.path.join(STORAGE_DIR, 'receipts')

    # Ограничения на файлы
    MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB (ограничение PythonAnywhere)
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB

    # Разрешенные расширения
    ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.avi'}
    ALLOWED_DOCUMENT_EXTENSIONS = {
        '.pdf', '.doc', '.docx', '.xls', '.xlsx',
        '.ppt', '.pptx', '.zip', '.txt'
    }
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.svg'}

    # Настройки бэкапов
    BACKUP_INTERVAL = 86400  # Раз в день
    MAX_BACKUPS = 10

    # Настройки логов
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # Настройки для видео
    VIDEO_CHUNK_SIZE = 1024 * 1024

    # Настройки пагинации
    ITEMS_PER_PAGE = 20

    # Настройки администратора по умолчанию
    DEFAULT_ADMIN = {
        'login': 'admin',
        'password': 'admin123',
        'full_name': 'Administrator',
        'email': 'bakhti0999@gmail.com',
        'phone': '+998994399968'
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev-secret-key-2026'
    SESSION_COOKIE_SECURE = False
    IS_PYTHONANYWHERE = False


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'production-secret-key-change-this')
    SESSION_COOKIE_SECURE = True
    IS_PYTHONANYWHERE = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATA_DIR = os.path.join(Config.BASE_DIR, 'test_data')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig  # По умолчанию production
}


def get_config():
    env = os.environ.get('FLASK_ENV', 'production')
    return config.get(env, ProductionConfig)()