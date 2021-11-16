FROM ubuntu:20.04
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/
WORKDIR cm-refurbish
COPY cm_refurbish/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY cm_refurbish .

# download missing datasets
ENV REPOREF="data"
ENV POPGJSN="LAU_RG_01M_2020_4326.geojson"
ENV BUILSTK="building_stock.csv"
# RUN wget -P ${REPOREF} https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/${POPGJSN}}
# RUN wget -P ${REPOREF} https://gitlab.com/hotmaps/building-stock/-/raw/master/data/${BUILSTK}

RUN python3 test.py
CMD ["python3", "worker.py"]
