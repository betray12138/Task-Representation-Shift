FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

COPY . /root/retro
COPY .mujoco /root/retro/.mujoco
RUN cd /root/retro \
 && mv .mujoco ~/.mujoco

ENV PATH="/root/miniconda3/bin:${PATH}" 

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh;

RUN conda init bash \
    && . ~/.bashrc \
    && conda create --name retro python=3.10 -y \
    && conda activate retro

RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse\ndeb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse\n" \
    > /etc/apt/sources.list \
    && apt-get update -y \
    && apt-get install libjpeg-dev zlib1g-dev -y\
    && apt install libosmesa6-dev libgl1-mesa-dev -y\
    && conda install -c anaconda libstdcxx-ng

RUN echo "MUJOCO_PY_MJPRO_PATH=~/.mujoco/mjpro131\nLD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/nvidia\nLD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.mujoco/mujoco210/bin" >> ~/.bashrc \
    && . ~/.bashrc

RUN cd /root/miniconda3/envs/retro/bin/../lib/ \
    && mv libstdc++.so.6 libstdc++.so.6.old \
    && ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 libstdc++.so.6

RUN cd /root/retro \
    conda init bash \
    && . ~/.bashrc \
    && conda activate retro \
    && pip install setuptools==59.5.0 \
    && pip install wheel==0.37.1 \
    && pip install cython==0.29.32 \
    && pip install patchelf \
    && pip install pyOpenGL -i https://pypi.douban.com/simple \
    && pip install -r requirements.txt \
    && pip install -U 'mujoco-py<2.2,>=2.1' \
    && pip install gin-config \
    && pip install scikit-learn \
    && pip install seaborn==0.11.2 \
    && pip install tensorboardX==2.6.2