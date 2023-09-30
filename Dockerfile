FROM ubuntu

ENV PGDATABASE $PGDATABASE
ENV PGHOST $PGHOST
ENV PGPASSWORD $PGPASSWORD
ENV PGPORT $PGPORT
ENV PGUSER $PGUSER

RUN apt-get update
RUN apt-get -y upgrade python3 python3-pip postgresql
RUN apt-get install -y python3 python3-pip postgresql
RUN pip install requests beautifulsoup4

WORKDIR /

COPY . ./