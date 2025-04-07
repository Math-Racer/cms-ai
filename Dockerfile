# This dockerfile puts llama3.2 in the image itself instead of downloading it at last step. 

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip curl

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN ollama serve & sleep 5 && ollama pull llama3.2 && pkill ollama

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ollama serve & sleep 5 && python3 app.py
