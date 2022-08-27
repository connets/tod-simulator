FROM carlasim/carla:0.9.13

USER root
WORKDIR /app
RUN rm /etc/apt/sources.list.d/cuda.list \
    && apt update \
    && apt install -y --no-install-recommends python3-dev python3-setuptools python3-pip \
    && pip3 install --upgrade pip \
    && pip3 install flask psutil
ENV LC_ALL=C.UTF-8 
ENV LANG=C.UTF-8
COPY app.py app.py
USER carla
CMD python3 -m flask run --host=0.0.0.0
