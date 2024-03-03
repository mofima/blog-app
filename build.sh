#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 

# Check if CREATE_SUPERUSER is set
if [[ $CREATE_SUPERUSER ]]; then
  # Assuming necessary environment variables are set
  python manage.py createsuperuser --no-input
fi