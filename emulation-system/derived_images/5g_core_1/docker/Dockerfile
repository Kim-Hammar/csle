# OS
FROM kimham/csle_5g_core_base:0.9.0
USER root

# 1. Add all scripts to the root directory
ADD start.sh subscriber_init.sh five_g_core_manager.py start_stop_5g.sh /

# 2. Add all config files to the open5gs directory
ADD amf.yaml upf.yaml nrf.yaml /etc/open5gs/

# 3. Apply permissions in a single RUN layer to save space
RUN chmod 777 /start.sh /subscriber_init.sh /five_g_core_manager.py /start_stop_5g.sh && \
    chmod 666 /etc/open5gs/amf.yaml /etc/open5gs/upf.yaml /etc/open5gs/nrf.yaml

# timezone env with default
ENV TZ=Europe/Stockholm

# SSH
RUN service ssh start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
