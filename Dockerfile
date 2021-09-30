FROM ipfs/go-ipfs:latest

ENV BOOTSTRAP_IP 172.17.0.2
ENV BOOTSTRAP_ID 12D3KooWEMjzdFL6YP1ovZEJot3mbCU4bgVtwedBxu4bYChi3Udp
ENV BOOTSTRAP_PORT_PROTOCOL tcp
ENV BOOTSTRAP_PORT 4001

COPY private_network_kernel.sh /usr/local/bin/start_ipfs
RUN chown ipfs:users /usr/local/bin/start_ipfs && chmod +x /usr/local/bin/start_ipfs
