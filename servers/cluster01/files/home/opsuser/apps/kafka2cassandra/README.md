# kafka2cassandra

These scripts run on cluster01 to receive the kafka feeds and pump the
data into cassandra. There's no complex processing here, so we've skipped
using something like storm or spark streaming.

The processes are launched and kept running by supervisor.

To install, copy the files to /home/opsuser/apps/kafka2cassandra folder
/home/opsuser/virtualenvs/kafka2cassandra and pip install requirements.txt
