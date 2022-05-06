#!/bin/bash
sudo apt-get -y update
#docker関連
sudo apt-get -y install ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo groupadd docker
sudo usermod -aG docker $(whoami)
#sysdig関連
sudo apt install -y sysdig
echo ""$(whoami)" ALL=NOPASSWD:/usr/bin/sysdig,/usr/bin/pkill" | sudo EDITOR='tee -a' visudo
#sysstatコマンド
sudo apt install -y sysstat
#freeコマンド
sudo apt install -y procps
#iperfコマンド
sudo apt install -y iperf
#python3関連
sudo apt install -y python3
sudo apt install -y python3-pip
pip3 install numpy
pip3 install matplotlib
