FROM python:3.8-slim-buster

WORKDIR /app
RUN apt update
RUN apt install -y wget fonts-noto-cjk
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN apt-get install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python", "main.py"]