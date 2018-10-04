on cluster02:/home/opsuser/apps/compass
docker build -t compass .
docker run -d --name=compass --restart=always -p 49154:80 compass
