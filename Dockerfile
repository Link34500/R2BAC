FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

COPY .env /app/.env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN useradd -m appuser
RUN chown -R appuser /app


RUN apt update && apt install -y git
RUN git clone https://github.com/Link34500/R2BAC.git .

RUN pip install --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt


USER appuser

EXPOSE 8000


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "r2bac.wsgi:application"]