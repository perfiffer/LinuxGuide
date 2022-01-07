iftop可以监控Linux下的实时网络流量，以及TCP/IP连接信息。可以用来排查服务器网络堵塞情况，查询出占用服务器网络带宽的ip地址，判断是否是正常的流量进入，如果不是，可以通过防火墙将该ip屏蔽。

如果想了解iftop更详细的信息，可以去iftop[官网](http://www.ex-parrot.com/~pdw/iftop/)查看。

## 0X01 安装
### 仓库安装
* Redhat或CentOS  
1.先安装epel-release源
```
$ yum -y install epel-release
```
2.再安装iftop
```
$ yum -y install iftop
```
* Debain或Ubuntu
```
$ apt-get install iftop
```

### 源码编译安装
1.安装依赖包
* Redhat或CentOS
```
$ yum -y install flex byacc libpcap ncurses ncurses-devel libpcap-devel
```
* Debain或Ubuntu
```
$ apt-get install flex byacc libpcap0.8 libncurses5
```

2.下载源码、编译、安装
```
$ wget http://www.ex-parrot.com/pdw/iftop/download/iftop-0.17.tar.gz
$ tar -zxvf iftop-0.17.tar.gz
$ cd iftop-0.17
$ ./configure
$ make && make install
```

## 0x02 使用说明
### 输出说明
运行iftop命令，可以看到如下画面
```
$ iftop
```
![iftop](images/iftop.png 'iftop运行结果')

最上方显示的是流量范围的刻度尺。  
=>和<=分别表示出站流量和进站流量。  
由上图可以看到，docker这台主机向17.16.3.1的这个ip发送了1.32kb的数据，接收的数据为208b。

* TX: 发送的流量
* RX: 接收的流量
* TOTAL: 总流量
* Cum: 运行iftop到当前时间截止的总流量
* peak: 流量峰值
* rates: 分别表示过去2s、10s、40s的平均流量

### 常用参数
```
-i: 指定需要监测的网卡，如iftop -i eth0，可通过ip命令或者ifconfig命令查看当前的服务器网卡
-B: 将输出以byte为单位显示网卡流量，默认是bit
-n: 将输出的主机信息都通过IP显示，不进行DNS解析
-N: 只显示连接端口号，不显示端口对应的服务名称
-F: 显示特定网段的网卡进出流量
-p: 以混杂模式运行iftop，此时iftop可以作为网络嗅探器使用
-P: 显示端口以及主机信息
-m: 设置输出界面中最上面的流量刻度最大值，流量刻度分5个大段显示，如iftop -m 10m
-f: 使用筛选码选择数据包来计数
-b: 不显示流量图形条
-c: 指定可选的配置文件
-t: 使用不带ncurses的文本界面，一般和-s、-L组合使用
-s: 指定秒数后打印一次文本输出然后退出，一般和-t组合使用，如iftop -t -s 60表示取60s的网络流量输出到终端
-L：指定打印的行数，一般和-t组合使用
-h: 显示帮助信息，可以通过iftop -h查看详细的参数信息
```

### 界面操作
```
#一般操作
p: 切换暂停/继续
h: 在交互界面/状态输出界面之间切换
b: 切换是否显示平均流量图形条
B: 切换显示2s、10s、40s内的平均流量
T: 切换是否显示每个连接的总流量
t：切换输出模式，一行或多行展示
j: 向上滚动屏幕显示当前连接信息
k: 向下滚动屏幕显示当前连接信息
f: 编辑筛选码
l: 打开输出过滤功能，即根据相关的条件进行搜索，如只查看固定IP的流量信息
L: 切换显示流量刻度范围，刻度不同，流量图形条也会不同
q: 退出界面显示
#显示主机信息
n: 使iftop输出结果以IP或主机名的方式显示
s: 切换是否显示源主机信息
d: 切换是否显示远端目标主机信息
#显示端口
N: 切换显示端口号/端口号对应的服务名称
S: 切换是否显示本地源主机的端口信息
D: 切换是否显示远端目标主机的端口信息
P：切换是否显示端口信息
#排序
1/2/3：分别通过第1列、第2列、第3列排序
<：根据左边的本地主机名或IP地址进行排序
>: 根据远端目标主机的主机名或IP地址进行排序
o: 切换是否固定显示当前的连接
```

## 0x03 使用示例
1.查看网卡eth0的信息，并显示IP和端口号
```
iftop -i eth0 -n -P
```
2.以byte为单位输出显示网卡流量
```
iftop -i eth0 -n -B
```
3.显示每个连接的总流量
```
iftop -i eth0 -n
#输入命令后按T
```
4.查找指定ip的流量
```
iftop -i eth0 -n
#输入命令后按l，输入要查询的ip，如17.16.3.129
```

## 0x04 实战演练
待定
---
