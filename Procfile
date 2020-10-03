release: python manage.py migrate
web: daphne chat.asgi:application --port $PORT --bind 0.0.0.0