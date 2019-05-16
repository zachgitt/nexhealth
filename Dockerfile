FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install jinja2
ENTRYPOINT ["python3"]
CMD ["app.py"]
