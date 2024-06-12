echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started"

# Run migrations
flask db upgrade

# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:5000 app:myapp