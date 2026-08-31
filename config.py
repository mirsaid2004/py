# config.py
import os
from datetime import timedelta


def _require_secret_key() -> str:
    """Читает SECRET_KEY из переменной окружения.

    Этим ключом Flask подписывает cookie сессий. Если ключ записан прямо
    в коде, любой, кто увидит исходники, сможет подделать cookie админа.
    Поэтому на сервере ключ обязателен, и без него приложение не стартует.
    """
    key = os.environ.get('SECRET_KEY')
    if not key:
        raise RuntimeError(
            "SECRET_KEY environment variable is not set.\n"
            "Add this to the top of your WSGI file, above the app import:\n"
            "    os.environ['SECRET_KEY'] = '<your-random-key>'\n"
            "Generate a key with:\n"
            '    python -c "import secrets; print(secrets.token_hex(32))"'
        )
    return key


class Config:
    # Базовые настройки
    # Внимание: этот ключ только для локальной разработки.
    # На сервере используется ProductionConfig, который берёт ключ из окружения.
    SECRET_KEY = 'dev-secret-key-change-in-production-2026'
    DEBUG = False  # На сервере всегда False
    TESTING = False

    # Настройки сессий
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # На сервере True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Корень проекта определяется по расположению этого файла.
    # Так путь верен и на сервере, и на локальной машине, и не зависит
    # ни от имени пользователя, ни от названия папки проекта.
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


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev-secret-key-2026'
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    def __init__(self):
        # Ключ берётся только из окружения, запасного значения в коде нет.
        self.SECRET_KEY = _require_secret_key()


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