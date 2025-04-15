FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN mkdir -p /vlr-api

WORKDIR /vlr-api

RUN python3 -m venv venv
RUN . venv/bin/activate

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN python3 -m 
COPY . .

RUN apk add curl

WORKDIR /api
CMD ["python", "mainapi.py"]