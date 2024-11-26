FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements_authz.txt requirements_authz.txt

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -r requirements_authz.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]