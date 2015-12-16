FROM acacia

RUN echo
RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libssl-dev &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y libcurl4-openssl-dev

ADD dreamboat/* /app/
RUN pip install -r /app/requirements.txt

COPY ship.d /etc/ship.d
