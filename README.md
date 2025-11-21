# 🎯 Django CRM - Sistema de Gestión de Clientes

Una aplicación Django moderna para gestionar clientes, compañías e interacciones con un diseño profesional.

## 📋 Características

- ✅ Gestión de **1000 clientes** con 3 representantes de ventas
- ✅ **~500,000 interacciones** (500 por cliente)
- ✅ Filtros avanzados (búsqueda, cumpleaños, ordenamiento)
- ✅ Diseño moderno con gradientes y efectos interactivos
- ✅ Formato de fechas en español
- ✅ Tiempo relativo para interacciones ("hace 2 días (Phone)")
- ✅ Paginación de 25 registros por página
- ✅ 100% Dockerizado con PostgreSQL

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)

```cmd
docker-compose up -d
```

El contenedor automáticamente:
1. ✅ Esperará a que PostgreSQL esté listo
2. ✅ Ejecutará las migraciones
3. ✅ Generará los datos de prueba (si no existen)
4. ✅ Iniciará el servidor en `http://localhost:8000`

### Opción 2: Local (Sin Docker)

1. **Instalar dependencias:**
```cmd
pip install -r requirements.txt
```

2. **Configurar base de datos** (editar `.env`):
```properties
DB_HOST=localhost
DB_PORT=5432
DB_NAME=db
DB_USER=postgres
DB_PASSWORD=password123
```

3. **Ejecutar migraciones:**
```cmd
python manage.py migrate
```

4. **Generar datos de prueba:**
```cmd
python manage.py generate_data
```

5. **Iniciar servidor:**
```cmd
python manage.py runserver
```

## Funcionalidades de la Vista CRM

### Búsqueda
- Busca por nombre de cliente o compañía
- URL: `/?q=nombre`

### Filtro de Cumpleaños
- Muestra clientes con cumpleaños esta semana
- URL: `/?birthday=this_week`

### Ordenamiento
- **Por nombre:** `/?sort=name`
- **Por compañía:** `/?sort=company`
- **Por cumpleaños:** `/?sort=birthday`
- **Por última interacción:** `/?sort=last_interaction`

## Estructura de Datos

### Modelos

- **Company:** Compañías (50 en total)
- **Customer:** Clientes (1000 en total)
  - Nombre completo
  - Compañía asociada
  - Representante de ventas
  - Cumpleaños
- **Interaction:** Interacciones (~500,000 en total)
  - Tipos: Phone, Email, SMS, Facebook
  - Timestamp
  - Notas

### Usuarios de Prueba

- `sales1` / password: `password`
- `sales2` / password: `password`
- `sales3` / password: `password`

## Tecnologías

- **Django 5.2.8** - Framework web
- **PostgreSQL 16** - Base de datos
- **Faker** - Generación de datos ficticios
- **Docker** - Contenedorización
- **Alpine Linux** - Imagen base ligera

## Comandos de Management

### Generar Datos Personalizados

```cmd
python manage.py generate_data --users 5 --companies 100 --customers 2000 --interactions-per-customer 300
```

## Autor

Desarrollado por EziC14
