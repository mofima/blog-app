#!/bin/bash
# exit on error
set -o errexit

# Print Bash version
echo "Bash Version: $BASH_VERSION"

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 

echo "Checking if CREATE_SUPERUSER is set..."
if [ "$CREATE_SUPERUSER" ]; then
    echo "CREATE_SUPERUSER is set. Proceeding to create superuser..."
    python manage.py createsuperuser --no-input
    echo "Superuser creation complete."
else
    echo "CREATE_SUPERUSER is not set. Skipping superuser creation."
fi
