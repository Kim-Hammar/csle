# OS
FROM kimham/csle_ubuntu_22_base:0.9.0
USER root

RUN apt-get update && \
    apt-get install -y curl software-properties-common ca-certificates && \
    add-apt-repository -y ppa:softwareradiosystems/srsran-project && \
    apt-get update && \
    apt-get install -y srsran-project