FROM python:2.7

ENV HTTP_PORT="8002"

RUN mkdir /warden && chmod 777 /warden
COPY . /warden

WORKDIR /warden
RUN pip install -r requirements.txt

EXPOSE 8002
