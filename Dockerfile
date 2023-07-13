FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update -y && apt-get install -y gcc

WORKDIR /app

COPY requirements.txt /app

RUN pip install opencv-python
RUN pip install pandas
RUN pip install psutil
RUN pip install pyyaml
RUN pip install tqdm
RUN pip install ultralytics
RUN pip install --no-cache-dir -r requirements.txt

COPY ./start.django.sh /start-django
RUN chmod +x /start-django

ADD . /app
