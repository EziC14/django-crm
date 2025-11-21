#!/bin/sh

echo "Esperando que PostgreSQL esté listo..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done
echo "PostgreSQL está listo!"

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Verificando si existen datos..."
CUSTOMER_COUNT=$(python manage.py shell -c "from api.models import Customer; print(Customer.objects.count())")

if [ "$CUSTOMER_COUNT" -eq "0" ]; then
  echo "Generando datos de prueba..."
  python manage.py generate_data --users 3 --companies 50 --customers 1000 --interactions-per-customer 500
  echo "Datos generados exitosamente!"
else
  echo "Ya existen $CUSTOMER_COUNT clientes en la base de datos. Omitiendo generación de datos."
fi

echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
