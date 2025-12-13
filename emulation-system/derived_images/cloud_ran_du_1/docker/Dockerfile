# OS
FROM kimham/csle_cloud_ran_base:0.9.0
USER root

# Add start scripts
ADD start.sh /start.sh
RUN chmod 777 /start.sh

ADD start_stop_du.sh /start_stop_du.sh
RUN chmod 777 /start_stop_du.sh

ADD start_stop_ue.sh /start_stop_ue.sh
RUN chmod 777 /start_stop_ue.sh

# Add config
ADD du.yml /srsRAN_Project/build/apps/du/du.yml
RUN chmod 666 /srsRAN_Project/build/apps/du/du.yml

ADD ue.conf /srsRAN_4G/build/srsue/src/ue.conf
RUN chmod 666 /srsRAN_4G/build/srsue/src/ue.conf

# timezone env with default
ENV TZ=Europe/Stockholm

# SSH
RUN service ssh start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
