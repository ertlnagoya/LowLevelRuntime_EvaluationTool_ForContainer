# Container_Eval_Tool_M1
 
こちらはコンテナ作成時に使用する低レベルランタイムの評価ツールです。
 
自動でベンチマークの実行、グラフとログの作成を行ってくれます。
 
# Features
 
合計12種類のベンチマークを用意しました。

* コンテナ内部の処理性能
* cpu
	* memory
	* file_rnd_read
	* file_seq_read
	* file_rnd_write
	* file_seq_write
	* syscall
	* network
* コンテナがホストで使用するリソース
	* lifecycle
	* resource_cpu
	* resource_memory
	* resource_storage

 
# Requirement
 
まとめ中です
 
# Installation
 
Docker
sysstat
 
# Usage
 
cpuベンチマークを実行するコマンド
 
```bash
source start_bench.sh cpu
```
 
# Note
 
dockerfileディレクトリは使用したコンテナイメージのDockerfileをまとめています。
tmpディレクトリはツールの作成時に実験的に作成したファイルをまとめています。
 
# Author
 
* Name
	* 西村 惇
* 所属
	* 名古屋大学大学院　情報学研究科　高田研究室　
* E-mail
	* atsushi_n@ertl.jp

