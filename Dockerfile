FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install logdelta

WORKDIR /app/demo

CMD ["tail","-f", "/dev/null"]