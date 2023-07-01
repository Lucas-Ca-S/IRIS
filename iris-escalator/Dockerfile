FROM python:3.10.10-slim-bullseye

COPY iris-escalator/ /iris-escalator/
WORKDIR /iris-escalator
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]
