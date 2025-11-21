FROM python:3.12-alpine

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Instalar dependencias del sistema
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    netcat-openbsd \
    bash

# Copiar e instalar dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copiar código de la aplicación
COPY . .

# Hacer ejecutable el script de entrada
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Usar el script de entrada
ENTRYPOINT ["./entrypoint.sh"]