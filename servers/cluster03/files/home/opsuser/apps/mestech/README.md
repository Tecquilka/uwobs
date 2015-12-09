# mestech data acquisition

Note ysi2mssql.py contains database credentials and should not be submitted
to git as is.

Install notes

    sudo apt-get install -y python-dev lib32z1-dev liblz-dev freetds-dev freetds-bin
    mkdir -p ~/dev
    cd ~/dev
    https_proxy=http://10.0.5.55:80 git clone https://github.com/edenhill/librdkafka.git
    cd librdkafka
    ./configure
    make
    sudo make install
    sudo ldconfig
    cd ~/dev
    https_proxy=http://10.0.5.55:80 git clone https://github.com/edenhill/kafkacat.git
    cd kafkacat
    ./configure
    make
    sudo make install
    mkdir -p ~/virtualenvs
    virtualenv ~/virtualenvs/mestech
    https_proxy=http://10.0.5.55:80 http_proxy=http://10.0.5.55:80 pip install -r requirements.txt
    sudo mkdir -p /data/mestech
    sudo chown opsuser:opsuser /data/mestech

The cron job is in cron.tab

The supervisor job is in mestech.conf also copied to /etc/supervisor/conf.d/mestech.conf

    

