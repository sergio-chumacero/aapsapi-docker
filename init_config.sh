python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_ADMIN_USER', '$DJANGO_ADMIN_MAIL', '$DJANGO_ADMIN_PASSWORD')" | python manage.py shell
python manage.py collectstatic --noinput