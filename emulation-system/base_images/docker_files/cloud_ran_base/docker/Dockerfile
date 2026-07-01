# OS
FROM kimham/csle_ubuntu_22_base:0.10.0
USER root

RUN apt-get update && \
    apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev \
    libyaml-cpp-dev libgtest-dev libzmq3-dev \
    git autoconf automake libtool

RUN git clone https://github.com/zeromq/czmq.git && \
    cd czmq && ./autogen.sh && ./configure && \
    make && make install && ldconfig

# The srsRAN Project transitioned to OCUDU in Dec 2025 and the repo's main branch was emptied
# down to a README, so pin to the last tagged release which still contains the source tree.
RUN git clone --depth 1 --branch release_25_10 https://github.com/srsran/srsRAN_Project.git && \
    cd srsRAN_Project && mkdir build && cd build && \
    cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON && \
    make -j $(nproc)

RUN apt-get update && \
    apt-get install -y build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev \
    libconfig++-dev libsctp-dev libzmq3-dev git && \
    git clone --depth 1 https://github.com/srsran/srsRAN_4G.git && \
    cd srsRAN_4G && mkdir build && cd build && cmake ../ && make srsue -j10
