#! /bin/bash
celery worker -A celery_app.celery --loglevel=info
