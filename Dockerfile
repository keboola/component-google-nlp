FROM python:3.6-alpine
ENV PYTHONIOENCODING utf-8

COPY . /code/

RUN dnf install python3-devel
RUN dnf install make automake gcc gcc-c++ gcc-gfortran
RUN dnf install redhat-rpm-config
RUN dnf install subversion


RUN apk add git
RUN pip install flake8

RUN pip install -r /code/requirements.txt



WORKDIR /code/


CMD ["python", "-u", "/code/src/component.py"]
