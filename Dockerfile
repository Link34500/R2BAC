FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip

COPY requirements.txt  /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser
RUN chown -R appuser /app

COPY . /app/

USER appuser

EXPOSE 8000

# Commande de production
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "r2bac.wsgi:application"]
# Commande de dévelopemment
CMD ["python","manage.py","runserver","0.0.0.0:8000"]