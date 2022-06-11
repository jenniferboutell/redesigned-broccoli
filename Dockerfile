FROM python:3.10.4-slim-bullseye

WORKDIR /usr/src/flask-project

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

CMD python app.py