# [日本語版はこちら](https://github.com/ertlnagoya/LowLevelRuntime_Evaluation_Tool_For_Container) 
# LowLevelRuntime_Evaluation_Tool_For_Container
It's an evaluation tool for low-level runtime of container.   
It automatically runs benchmarks and generates graphs and logs.  
Graphs and logs are generated under the directory of the executed item.   

# Features
14 types of benchmarks are available.    
### Performance inside the container
* cpu  
* memory
* file_rnd_read
* file_seq_read
* file_rnd_write
* file_seq_write
* syscall
* network
### Resources used by the container on the host
* lifecycle
* resource_cpu
* resource_memory
* resource_storage
### Security for low-level runtime (Under development)
* syscall_collect
* runtime_cve
* AbstractResource_AttackProgram

# Requirement
Make sure the following commands are available.  
All commands are available by running package_install.sh.  
However, read the following descriptions for journalctl and low-level runtime and configure them on your own.   
### docker  
Install docker, to refer to the [link](https://matsuand.github.io/docs.docker.jp.onthefly/engine/install/ubuntu/).  
After installation, change the privileges to use docker command without sudo.  
```bash
$ sudo groupadd docker
$ sudo usermod -aG docker user-name
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
In resource_storage, the size of system.journal may affect the results.  
Therefore, modify /etc/systemd/journald.conf so that journald does not collect logs.  
Once the benchmark is finished, you may return to the original settings.  
If you want to include the size of the logs in your evaluation, need not to change the settings.  
And restart the system at each low-level runtime to restore the logs.   
```bash
$ sudo vi /etc/systemd/journald.conf
```  
Change a part of /etc/systemd/journald.conf as follows.  
```bash
[Journal]
Storage=none
```
After changing, reflect to the configuration file following command.   
```bash
$ sudo systemctl daemon-reload 
$ sudo systemctl restart systemd-journald.service
```  

# Installation
### LowLevelRuntime_Evaluation_Tool_For_Container  
Clone this repository from github.  
```bash
$ git clone https://github.com/ertlnagoya/LowLevelRuntime_Evaluation_Tool_For_Container/
```
### low-level runtime  
[](This tool use [runc](https://github.com/opencontainers/runc)、[crun](https://github.com/containers/crun)、[runsc](https://gvisor.dev/docs/user_guide/install/) by default.  )
If necessary, install the low-level runtime you want to evaluate.  
After installation, write the link of the low-level runtime to /etc/docker/daemon.  
However, you can use [runc](https://github.com/opencontainers/runc) after installing docker without writing link to /etc/docker/daemon.json.  

Refer to following example of installing [crun](https://github.com/containers/crun).  
```bash
#Install the dependent tools for crun.
$ sudo apt-get install -y make git gcc build-essential pkgconf libtool \
    libsystemd-dev libprotobuf-c-dev libcap-dev libseccomp-dev libyajl-dev \
    go-md2man libtool autoconf python3 automake
$ git clone https://github.com/containers/crun

#Install crun.
$ cd crun-directory
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install

#Set /etc/docker/daemon.json to use crun with docker.
$ sudo vi /etc/docker/daemon.json
```  
Change /etc/docker/daemon.json as follows.
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
### To measure performance inside the container (e.g. cpu) 
Write low-level runtime name to cpu.sh in the cpu directory, (e.g. crun and runsc).
```bash
declare -a low_level_runtime=("crun" "runsc")
```
Run start_bench.sh with specify the cpu item as an argument.
```bash
$ source start_bench.sh cpu
```
### To measures resources used by the container on the host (e.g. syscall_collect) 
Write low-level runtime name to syscall_collect.sh in the syscall_collect directory, (e.g. crun and runsc).
```bash
declare -a low_level_runtime=("crun" "runsc")
```
Run start_bench.sh with specify the syscall_collect item and container image(and command) as an argument.
```bash
$ source start_bench.sh syscall_collect "paipoi/sysbench_"$(uname -p)" sysbench --test=cpu --cpu-max-prime=20000 --num-threads=1 run"
```
### To execute Abstract Resource Attack (e.g. AbstractResource_AttackProgram) 
Since a directory is provided for each Abstract Resource, inside the container, you execute the attack program in each directory.

# Note
* I have confirmed operation on x86_64 Ubuntu 18.04 and Ubuntu 20.04 and aarch64 Ubuntu 20.04 to specify runc and crun,runsc, kata.  
* The dockerfile directory is a collection of Dockerfiles for the container images used.  
* The tmp directory is a collection of experimental files created when the tool was created.


# Licence

* This tool (LowLevelRuntime_Evaluation_Tool_For_Container) is released under the [MIT license](https://github.com/ertlnagoya/LowLevelRuntime_Evaluation_Tool_For_Container/blob/master/LICENSE).    
* Licenses for libraries, software, etc. used in this tool are as follows.  

| Software・Library | License |
| :---: | :---: |
| docker engine | [Apache License Version 2.0](https://docs.docker.jp/engine/faq.html#what-open-source-license-are-you-using) |
| sysstat | [GNU General Public License v2.0](https://github.com/sysstat/sysstat/blob/master/COPYING) |
| sysdig | [Apache License Version2.0](https://github.com/draios/sysdig/blob/dev/NOTICES) |
| sysbench(Used in container image) | [GNU General Public License v2.0](https://github.com/akopytov/sysbench/blob/master/COPYING) |
| unixbench(Used in container image) | [GNU General Public License v2.0](https://github.com/kdlucas/byte-unixbench/blob/master/LICENSE.txt) |
| iper3(Used in container image) | [BSD License](https://github.com/esnet/iperf/blob/master/LICENSE) |
| numpy | BSD License(Checked with pip-licenses) |
| matplotlib | BSD License(Checked with pip-licenses) |
| selenium | Apache Software License(Checked with pip-licenses) |
| geckodriver | [Mozilla Public License](https://github.com/mozilla/geckodriver#source-code) |


# Author
#### Name  
Nishimura Atsushi
#### Affiliation  
Takada Laboratory, Graduate School of Informatics, Nagoya University　
#### E-mail  
atsushi_n@ertl.jp
