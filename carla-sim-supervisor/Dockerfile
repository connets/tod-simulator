FROM carlasim/carla:0.9.13

USER root
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN rm /etc/apt/sources.list.d/cuda.list \
    && apt update \
    && apt install -y --no-install-recommends python3-dev python3-setuptools python3-pip xdg-user-dirs xdg-utils \
    && pip3 install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
    #&& pip3 install zerorpc psutil
ENV LC_ALL=C.UTF-8 
ENV LANG=C.UTF-8
COPY sim_controller.py sim_controller.py
USER carla
CMD python3 sim_controller.py /home/carla/CarlaUE4.sh
#CMD python3 -m flask run --host=0.0.0.0
