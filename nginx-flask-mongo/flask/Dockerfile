FROM python:3.7

WORKDIR /src
COPY . .
RUN pip install -r requirements.txt --no-cache-dir

RUN splunk-py-trace-bootstrap

CMD ["python3", "./server.py"]
