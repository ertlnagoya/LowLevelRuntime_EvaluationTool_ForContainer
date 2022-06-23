# [English version is here](https://github.com/ertlnagoya/Container_Eval_Tool_M1/blob/master/README%20_en.md)  
# Container_Eval_Tool_M1
コンテナ作成時に使用する低レベルランタイムの評価ツールです。   
自動でベンチマークの実行、グラフとログの生成を行います。  
グラフとログは実行した項目のディレクトリ下に生成されます。

# Features
合計13種類のベンチマークを用意しました。  
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
### 低レベルランタイムのセキュリティ(開発途中)
* gompertz_cve
* syscall_collect

# Requirement
以下の全てのコマンドが使用できることを確認して下さい。  
package_install.shを実行することで以下のコマンドを使用できるようになります。  
ただし、journalctlと低レベルランタイムに関しては以下の記述を読んで、各自で設定を行ってください。  
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
### iperf3  
```bash
$ sudo apt install -y iperf3
```
### sysdig  
```bash
$ sudo apt install -y sysdig
$ echo ""$(whoami)" ALL=NOPASSWD:/usr/bin/sysdig,/usr/bin/pkill" | sudo EDITOR='tee -a' visudo
```
### python3 (+pip3,numpy,matplotlib,selenium)  
```bash
$ sudo apt install -y python3
$ sudo apt install -y python3-pip
$ pip3 install numpy
$ pip3 install matplotlib
$ pip3 install selenium
```
### geckodriver
```bash
$ curl -OL https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
$ tar -zxvf geckodriver-v0.31.0-linux64.tar.gz
$ sudo cp geckodriver /usr/local/bin/geckodriver
```
### journalctl  
resource_storageではsystem.journalのサイズが結果に影響を及ぼしかねません。  
そのため、/etc/systemd/journald.confを変更し、journaldでログを収集しないように変更します。  
ベンチマークが終了したら、元の設定に戻しても構いません。  
ログのサイズも含めて評価する場合、設定の変更を行わず、低レベルランタイム毎にシステムを再起動してログをもとに戻して下さい。
```bash
$ sudo vi /etc/systemd/journald.conf
```  
/etc/systemd/journald.confの一部を以下のように変更します。  
```bash
[Journal]
Storage=none
```
変更後は、以下のコマンドで設定ファイルの内容を反映させて下さい。  
```bash
$ sudo systemctl daemon-reload 
$ sudo systemctl restart systemd-journald.service
```  

# Installation
### Container_Eval_Tool_M1  
githubからこのリポジトリをクローンして下さい。  
```bash
$ git clone https://github.com/ertlnagoya/Container_Eval_Tool_M1/
```
### 低レベルランタイム  
[](デフォルトで[runc](https://github.com/opencontainers/runc)、[crun](https://github.com/containers/crun)、[runsc](https://gvisor.dev/docs/user_guide/install/)を使用するように設定しています。  )
必要に応じて、評価したい低レベルランタイムをインストールして下さい。  
インストール後、/etc/docker/daemon.jsonに低ベレルランタイムのリンク先を記入して下さい。  
ただし、[runc](https://github.com/opencontainers/runc)は/etc/docker/daemon.jsonに記入せずとも、dockerをインストールした時点で使用できます。  

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
### コンテナ内部の処理性能を計測する場合(例：cpu) 
cpuディレクトリのcpu.shに、評価対象とする低レベルランタイム（以下の例はcrun、runsc）を記入します。
```bash
declare -a low_level_runtime=("crun" "runsc")
```
引数としてcpu項目を指定し、start_bench.shを実行します。
```bash
$ source start_bench.sh cpu
```
### コンテナがホストで使用するリソースを計測する場合(例：syscall_collect) 
syscall_collectディレクトリのsyscall_collect.shに、評価対象とする低レベルランタイム（以下の例はcrun、runsc）を記入します。
```bash
declare -a low_level_runtime=("crun" "runsc")
```
引数としてsyscall_collect項目とコンテナイメージ(+コマンド)を指定し、start_bench.shを実行します。
```bash
$ source start_bench.sh syscall_collect "paipoi/sysbench_"$(uname -p)" sysbench --test=cpu --cpu-max-prime=20000 --num-threads=1 run"
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
