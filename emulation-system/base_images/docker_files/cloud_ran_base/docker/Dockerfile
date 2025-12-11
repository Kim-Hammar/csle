# OS
FROM kimham/csle_ubuntu_22_base:0.9.0
USER root

# OS
FROM kimham/csle_ubuntu_22_base:0.9.0
USER root

RUN apt-get update && \
    apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev \
    libyaml-cpp-dev libgtest-dev libzmq3-dev \
    git autoconf automake libtool

RUN git clone https://github.com/zeromq/czmq.git && \
    cd czmq && ./autogen.sh && ./configure && \
    make && make install && ldconfig

RUN git clone https://github.com/srsran/srsRAN_Project.git && \
    cd srsRAN_Project && mkdir build && cd build && \
    cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON && \
    make -j $(nproc)
