# OS
FROM kimham/csle_cloud_ran_base:0.9.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

ADD start_stop_cu.sh /start_stop_cu.sh
RUN chmod 777 /start_stop_cu.sh

# Add config
ADD cu.yml /srsRAN_Project/build/apps/cu/cu.yml
RUN chmod 666 /srsRAN_Project/build/apps/cu/cu.yml

# timezone env with default
ENV TZ=Europe/Stockholm

# SSH
RUN service ssh start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
