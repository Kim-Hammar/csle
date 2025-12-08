# OS
FROM kimham/csle_ubuntu_22_base:0.9.0
USER root

# MongoDB
RUN apt update
RUN apt install gnupg
RUN curl -fsSL https://pgp.mongodb.com/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
RUN update
RUN apt install -y mongodb-org
RUN systemctl start mongod
RUN systemctl enable mongod