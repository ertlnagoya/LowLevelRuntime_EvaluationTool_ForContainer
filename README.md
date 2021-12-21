# Container_Eval_Tool_M1
コンテナ作成時に使用する低レベルランタイムの評価ツールです。   
自動でベンチマークの実行、グラフとログの作成を行います。

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
以下の全てのコマンドが使用できることを確認して下さい。  
### docker  
[リンク先](https://matsuand.github.io/docs.docker.jp.onthefly/engine/install/ubuntu/)を参考にDockerをインストールして下さい。  
インストール後に、sudo権限なしでdockerコマンドを実行できるように変更して下さい。  
```bash
$ sudo groupadd docker
$ sudo usermod -aG docker ユーザ名
$ sudo reboot
```
### sysstat  
```bash
$ sudo apt install -y sysstat
```
### free  
```bash
$ sudo apt install -y procps
```
### iperf  
```bash
$ sudo apt install -y iperf
```
### python3 (+pip3,numpy,matplotlib)  
```bash
$ sudo apt install -y python3
$ sudo apt install -y python3-pip
$ pip3 install numpy
$ pip3 install matplotlib
```

# Installation
### Container_Eval_Tool_M1  
githubからこのリポジトリをクローンして下さい。  
```bash
$ git clone https://github.com/ertlnagoya/Container_Eval_Tool_M1/
```
### 低レベルランタイム  
デフォルトで[crun](https://github.com/containers/crun)と[runsc](https://gvisor.dev/docs/user_guide/install/)を使用するように設定しています。  
必要に応じて、評価したい低レベルランタイムをインストールして下さい。  
その後、/etc/docker/daemon.jsonに低ベレルランタイムのリンク先を記入して下さい。  
以下に、[crun](https://github.com/containers/crun)をインストールする例を載せますので参考にして下さい。  
```bash
#crunに必要な依存ツールをインストールします。
$ sudo apt-get install -y make git gcc build-essential pkgconf libtool \
    libsystemd-dev libprotobuf-c-dev libcap-dev libseccomp-dev libyajl-dev \
    go-md2man libtool autoconf python3 automake
$ git clone https://github.com/containers/crun

#crunをインストールします。
$ cd crunのディレクトリ
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install

#dockerでcrunを使用できるように、/etc/docker/daemon.jsonへ書き込みを行います。
$ sudo vi /etc/docker/daemon.json
```  
/etc/docker/daemon.jsonの中身を以下のように変更します。
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
### cpuベンチマークを実行する場合 
cpuディレクトリのcpu.shに、評価対象とする低レベルランタイム（以下の例はcrun、runsc）を記入します。
```bash
declare -a low_level_runtime=("crun" "runsc")
```
引数としてcpu項目を指定し、start_bench.shを実行します。
```bash
$ source start_bench.sh cpu
```

# Note
* x86_64のUbuntu18.04とUbuntu20.04、aarch64のUbuntu20.04において、crunとrunscを指定した際の動作を確認しました。  
* dockerfileディレクトリは使用したコンテナイメージのDockerfileをまとめています。  
* tmpディレクトリはツールの作成時に実験的に作成したファイルをまとめています。

# Author
#### 名前（Name）  
西村 惇（Nishimura Atsushi）
#### 所属  
名古屋大学大学院　情報学研究科　高田研究室　
#### E-mail  
atsushi_n@ertl.jp
