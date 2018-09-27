FROM nodered/node-red-docker
RUN npm install mailparser
RUN npm install node-red-contrib-cassandra
RUN npm install node-red-contrib-kafka-node
COPY config/flows.json /data/
COPY config/flows_cred.json /data/
COPY config/settings.js /data/
COPY config/config.json /data/.config.json
COPY config/package.json /data/
