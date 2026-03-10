FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install django djangorestframework psycopg2-binary
RUN pip install requests beautifulsoup4 feedparser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
