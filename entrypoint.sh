#!/bin/sh

echo "⏳ Esperando que PostgreSQL esté listo..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done
echo "✅ PostgreSQL está listo!"

echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "🎲 Generando datos de prueba (si no existen)..."
python manage.py generate_data --users 3 --companies 50 --customers 1000 --interactions-per-customer 500

echo "🚀 Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
