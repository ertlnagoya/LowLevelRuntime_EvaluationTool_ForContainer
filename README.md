# Container_Eval_Tool_M1
 
こちらはコンテナ作成時に使用する低レベルランタイムの評価ツールです。
 
自動でベンチマークの実行、グラフとログの作成を行ってくれます。
 
# Features
 
合計12種類のベンチマークを用意しました。

### コンテナ内部の処理性能
* cpu
* memory
* file_rnd_read
* file_seq_read
* file_rnd_write
* file_seq_write
* syscall
* network
### コンテナがホストで使用するリソース
* lifecycle
* resource_cpu
* resource_memory
* resource_storage

 
# Requirement
 
以下の全てのコマンドが使用できることを確認してください

### docker  
[リンク先](https://matsuand.github.io/docs.docker.jp.onthefly/engine/install/ubuntu/)を参考にDockerをインストール  
インストール後に、sudo権限なしでdockerコマンドを実行できるように変更  
```bash
sudo groupadd docker
sudo usermod -aG docker ユーザ名
sudo reboot
```

### sysstat  
```bash
sudo apt install -y sysstat
```

### free  
```bash
sudo apt install -y procps
```

### python3 (ライブラリ含む)  
```bash
sudo apt install -y python3
sudo apt install -y python3-pip
pip3 install numpy
pip3 install matplotlib
```
 
# Installation

githubからこのリポジトリをクローンする  
```bash
git clone https://github.com/ertlnagoya/Container_Eval_Tool_M1/
```
<br>
必要に応じて低レベルランタイムをインストールする  

その後、/etc/docker/daemon.jsonに低ベレルランタイムのリンク先を記入  

### [crun](https://github.com/containers/crun)の場合
```bash
#依存ツールをインストール
sudo apt-get install -y make git gcc build-essential pkgconf libtool \
   libsystemd-dev libprotobuf-c-dev libcap-dev libseccomp-dev libyajl-dev \
   go-md2man libtool autoconf python3 automake
git clone https://github.com/containers/crun

#crunのインストール
cd crunのディレクトリ
./autogen.sh
./configure
make
sudo make install

#dockerでcrunを使用できるように書き込み
sudo vi /etc/docker/daemon.json
```
  
### /etc/docker/daemon.jsonの中身
```bash
{
    "runtimes": {
        "crun": {
            "path": "/usr/local/bin/crun"
        },
    },
}
```
 
# Usage
 
cpuベンチマークを実行するコマンド
```bash
source start_bench.sh cpu
```
 
# Note
 
* dockerfileディレクトリは使用したコンテナイメージのDockerfileをまとめています。

* tmpディレクトリはツールの作成時に実験的に作成したファイルをまとめています。
 
# Author
 
* Name
	* 西村 惇
* 所属
	* 名古屋大学大学院　情報学研究科　高田研究室　
* E-mail
	* atsushi_n@ertl.jp

