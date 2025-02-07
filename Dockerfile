FROM python:3.11

WORKDIR /app

COPY . /app

WORKDIR /app/demo/label_investigation

RUN pip install logdelta

WORKDIR /app/demo
RUN wget -O Hadoop.zip https://zenodo.org/records/8196385/files/Hadoop.zip?download=1
RUN unzip Hadoop.zip -d Hadoop
WORKDIR /app/demo

#CMD ["python", "-m", "logdelta.config_runner", "-c", "/app/demo/config.yml"]
CMD ["tail","-f", "/dev/null"]