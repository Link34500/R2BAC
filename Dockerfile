FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

COPY . /app/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN useradd -m appuser
RUN chown -R appuser /app


RUN apt update && apt install -y git

RUN pip install --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt

RUN python src/manage.py collectstatic --noinput
RUN python src/manage.py makemigrations
RUN python src/manage.py migrate


USER appuser

EXPOSE 8000


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "src.r2bac.wsgi:application"]