FROM python:3.6-alpine
ENV PYTHONIOENCODING utf-8

COPY . /code/
RUN apk add git
RUN pip install flake8
RUN ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install --upgrade numpy

RUN pip install -r /code/requirements.txt



WORKDIR /code/


CMD ["python", "-u", "/code/src/component.py"]
