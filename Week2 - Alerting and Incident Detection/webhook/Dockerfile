FROM python:3.10-slim

WORKDIR /app

COPY webhook_receiver.py .

RUN pip install flask

EXPOSE 9000

CMD ["python", "webhook_receiver.py"]
