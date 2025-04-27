FROM python:3.13.2-slim

WORKDIR /app
RUN mkdir -p /downloads
COPY ./app .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

#CMD ["python", "main.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
