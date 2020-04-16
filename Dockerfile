FROM python:3.7

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade -r requirements.txt

CMD ["python", "-u", "main.py"]