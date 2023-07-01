FROM python:3.10.10-slim-bullseye

COPY iris/ /iris/
WORKDIR /iris
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install curl -y
RUN apt-get install iputils-ping -y
RUN apt-get install telnet -y

ENTRYPOINT ["python"]
CMD ["main.py"]
