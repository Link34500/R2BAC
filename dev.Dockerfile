FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN useradd -m appuser
RUN chown -R appuser /app

COPY requirements.txt /app/

# RUN apt update && apt install -y git
# RUN git clone https://github.com/Link34500/R2BAC.git .

RUN pip install --upgrade pip

# COPY requirements.txt  /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

USER appuser

EXPOSE 8000

# Commande de production
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "r2bac.wsgi:application"]
# Commande de dévelopemment
CMD ["python","src/manage.py","runserver","0.0.0.0:8000"]