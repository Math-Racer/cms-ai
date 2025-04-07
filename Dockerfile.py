# Tested and it works like a charm!!


FROM python:3.10-slim

# Install curl and procps
RUN apt-get update && apt-get install -y curl procps

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN ollama serve & sleep 5 && ollama pull llama3.2 && pkill ollama

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt



CMD ["sh", "-c", "ollama serve & sleep 5 && python3 app.py"]

# Use `docker run -e WEBSITE_LINK=http://192.168.6.59:12345/api/v4/ -e CID=1 cms-ai`

# docker run passes the environment variables as string by default