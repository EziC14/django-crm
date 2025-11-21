FROM python:3.12-alpine

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]