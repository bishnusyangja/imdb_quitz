#! /bin/bash
celery worker -A main.celery --loglevel=info