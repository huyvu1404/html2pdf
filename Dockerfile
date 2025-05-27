FROM python:3.13-slim

RUN apt-get update && apt-get install -y wkhtmltopdf libxrender1 libfontconfig1 libxext6 \
    && apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
