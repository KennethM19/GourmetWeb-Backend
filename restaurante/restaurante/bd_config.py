from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

BD_POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'restaurante',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

BD_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistema_seguridad',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

BD_SQLITE3 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
