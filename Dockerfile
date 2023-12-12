FROM python:3.10

ADD . .

RUN pip install paho-mqtt

CMD ["python", "./src/messageQueue.py"]