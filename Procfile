web: gunicorn --worker-class gevent --timeout 600 --bind 0.0.0.0:$PORT --max-requests 250 inspinia.main:app
worker: celery worker --app=inspinia.tasks