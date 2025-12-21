# OS
FROM kimham/csle_ubuntu_22_base:0.9.0
USER root

# Arguments
ARG PACKAGE=open5gs
ARG VERSION=2.7.2
ARG DEBIAN_FRONTEND=noninteractive

# 1. System Setup
RUN mkdir -p /data/db \
    && mkdir -p /etc/apt/keyrings \
    && apt-get update && apt-get install -y \
       gnupg \
       curl \
       software-properties-common \
       ca-certificates \
    # MongoDB Key & Repo
    && curl -fsSL https://pgp.mongodb.com/server-8.0.asc | gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor \
    && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list \
    # Open5GS Repo
    && add-apt-repository -y ppa:open5gs/latest \
    # NodeJS Key & Repo
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && NODE_MAJOR=20 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    # Install Packages
    && apt-get update && apt-get install -y \
       mongodb-org \
       open5gs \
       nodejs \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# 2. Open5GS WebUI Build
RUN (id -u open5gs &>/dev/null || useradd -r -m -s /bin/false open5gs) \
    # Download directly to root
    && curl -sLf "https://github.com/open5gs/${PACKAGE}/archive/v${VERSION}.tar.gz" | tar zxf - \
    # Enter directory (located at /open5gs-2.7.2/webui)
    && cd "${PACKAGE}-${VERSION}/webui" \
    && npm clean-install \
    && npm run build \
    # Move artifacts
    && mkdir -p /usr/lib/node_modules \
    && mv "/${PACKAGE}-${VERSION}/webui" "/usr/lib/node_modules/${PACKAGE}" \
    && chown -R open5gs:open5gs "/usr/lib/node_modules/${PACKAGE}" \
    # Copy init script from root source
    && cp "/${PACKAGE}-${VERSION}/docs/assets/webui/mongo-init.js" /usr/lib/node_modules/${PACKAGE}/mongo-init.js \
    # Cleanup source files from root
    && rm -rf "/${PACKAGE}-${VERSION}" \
    && sysctl -w net.ipv4.ip_forward=1 \
    && sysctl -w net.ipv6.conf.all.forwarding=1
