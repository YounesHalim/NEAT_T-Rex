FROM gitpod/workspace-full-vnc

RUN sudo apt-get update && sudo apt-get install -y \
    python3.10 \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsdl1.2-dev \
    libsmpeg-dev \
    python3-numpy \
    subversion \
    libportmidi-dev \
    ffmpeg \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*
