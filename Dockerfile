FROM python:3.13-slim
RUN mkdir -p /vlr-api

WORKDIR /vlr-api

RUN python3 -m venv venv
RUN . venv/bin/activate

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
EXPOSE 8000
CMD  [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]