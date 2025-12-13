# OS
FROM kimham/csle_5g_core_base:0.9.0
USER root

# Add start scripts
ADD start.sh /start.sh
RUN chmod 777 /start.sh

ADD subscriber_init.sh /subscriber_init.sh
RUN chmod 777 /subscriber_init.sh

ADD five_g_core_manager.py /five_g_core_manager.py
RUN chmod 777 /five_g_core_manager.py

# timezone env with default
ENV TZ=Europe/Stockholm

# SSH
RUN service ssh start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
