#!/bin/bash

set -e


# goddamn latin-1 -> utf-8
# http://seanh.cc/posts/fix-postgresql-locale-on-vagrant/
# setup local for UTF-8 encoding in postgres
echo "export LANGUAGE=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LANG=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LC_ALL=en_US.UTF-8" >> /etc/bash.bashrc
locale-gen en_US.UTF-8
dpkg-reconfigure locales

. /etc/default/locale

# postgres 9.4:
echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >> /etc/apt/sources.list.d/pgdg.list

apt-get update
apt-get -y install python-software-properties
apt-get -y --force-yes install git \
                   postgresql-9.4 \
                   postgresql-contrib \
                   postgresql-server-dev-9.4 \
                   libpq-dev \
                   redis-server \
                   python \
                   python-dev \
                   python-pip \
                   python-setuptools \
                   build-essential \
                   gcc \
                   g++ \
                   python-lxml \

apt-get -y autoremove

# POSTGRES

# password-less logins
cp /vagrant/pg_hba.conf /etc/postgresql/9.4/main/pg_hba.conf
service postgresql restart

pg_dropcluster 9.4 main --stop
pg_createcluster 9.4 main --start
sudo -u postgres psql -l

pip install pgxnclient
pgxn install multicorn
sudo -u postgres psql template1 -c "create extension multicorn"
sudo -u postgres createdb pooshield
sudo -u postgres psql -c "CREATE USER vagrant"
sudo -u postgres psql -c "ALTER USER vagrant CREATEDB"
sudo -u postgres psql -c "ALTER DATABASE pooshield OWNER TO vagrant"


# PYTHON

echo 'PYTHONPATH=.' >> /home/vagrant/.bashrc

pip install -r requirements.txt
pip install -r requirements-dev.txt
# local development
pip install -e emailfdw

echo "Done!"
