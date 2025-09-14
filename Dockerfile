FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -m appuser
RUN chown -R appuser /app
RUN chmod +x entrypoint.sh

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

USER appuser

EXPOSE 8000

CMD ["./entrypoint.sh"]
