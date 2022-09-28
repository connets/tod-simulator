FROM python:3.8.13-bullseye
USER root
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py init.json ./

ARG seeds
ENV seeds ${seeds}
CMD for s in $seeds; do \
    python main.py init.json $s \
    sleep 10; \
    done;
