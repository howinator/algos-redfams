#!/usr/bin/env bash

set -ex

installpy(){

     apt-get -y update &&  apt-get -y upgrade
     apt-get -y install build-essential checkinstall
     apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev virtualenv postgresql-client

     cd /usr/src
     wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
     tar xzf Python-3.6.1.tgz

     cd Python-3.6.1
     ./configure
     make altinstall
}

installpy

{
    mkdir /opt/apps
} || {
    echo "/opt/apps already there"
}

cd /opt/apps
rm -rf algos-redfams
{
    git clone https://github.com/howinator/algos-redfams.git
} || {
    echo "repo allready there"
}

cd algos-redfams
virtualenv -p $(which python3.6) reddit-venv --no-site-packages
source reddit-venv/bin/activate
pip install -r requirements.txt

gsutil cp gs://howinator-config/creds.yml /opt/apps/algos-redfams/infra/vars/creds.yml
python ./scrape-entry.py prod
