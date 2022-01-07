介绍一款网络检测神器，ss（Socket Statistics），主要用来统计socket连接的相关信息，功能和netstat相似，但是更为强大。

ss相比与netstat的优势在于，它利用了TCP协议栈中的tcp_diag。tcp_diag是一个用于分析统计的模块，可以很快速的获取Linux内核中的信息，保证了ss的高效，在服务器有大量连接的时候，用ss无疑比netstat更节省时间。

## 安装
ss命令属于iproute工具集，所以安装iproute工具包即可。
```
#redhat、centos
yum install iproute iproute-doc -y
#debain、ubuntu
apt-get install iproute iproute-doc
```

## 命令使用
### 帮助命令
```
#获取帮助信息
ss -h, --help
#或者查看man手册
man ss
```

### 基本命令
```
-V, --version 查看ss版本信息
-H, --no-header  不展示表头信息
-n, --numeric 不解析服务名称
-r, --resolve 解析主机名
-a, --all 显示所有socket连接
-l, --listening 显示处于监听状态的socket连接
-o, --options 显示计时器信息
-e, --extended 显示详细的socket连接信息
-m, --memory 显示socket连接的内存使用情况
-p, --processes 显示使用socket的进程
-i, --info 显示TCP内部信息
-K, --kill 试图强制关闭套接字。此选项显示已成功关闭的套接字，并以静默方式跳过内核不支持关闭的套接字。它只支持IPv4和IPv6套接字
-Z, --context 类似于-p，但是会显示安全的进程上下文，需要开启selinux
-z, --contexts 类似于-Z，但是会显示安全的套接字上线文，需要开启selinux
-N NSNAME, --net=NSNAME 切换到指定的namespace网络，namespace需要自己指定，可使用ip netns工具包创建
-b, --bpf 显示socket BPF过滤器，只有管理员有权查看
-s, --summary 显示socket统计信息
-4, --ipv4 仅显示IPv4的socket连接
-6, --ipv6 仅显示IPv6的socket连接
-0, --packet 显示PACKET socket连接
-t, --tcp 仅显示tcp类型的socket连接
-u, --udp 仅显示udp类型的socket连接
-d, --dccp 仅显示dccp类型的socket连接
-w, --raw 仅显示raw类型的socket连接
-x, --unix 仅显示unix类型的socket连接
-S, --sctp 仅显示sctp套接字
--vsock 显示vsock套接字，是-f vsock的命令别名
-f, --family=FAMILY 显示FAMILY类型的socket连接，FAMILY可选，支持unix, inet, inet6, link, netlink, vsock
-A, --query=QUERY, --socket=QUERY  查询指定类型的socket连接，QUERY可选，支持all, inet, tcp, udp, raw, unix, packet, netlink
-D, --diag=FILE 将原始的TCP类型socket连接信息转储到文件
-F, --filter=FILE 从文件中获取过滤器信息
```

### 使用示例
#### 按照网络传输类型获取统计信息
```
$ ss -s
Total: 534 (kernel 1213)
TCP:   8 (estab 1, closed 1, orphaned 0, synrecv 0, timewait 0/0), ports 0

Transport Total     IP        IPv6
*	  1213      -         -        
RAW	  0         0         0        
UDP	  8         5         3        
TCP	  7         5         2        
INET	  15        10        5        
FRAG	  0         0         0
```
#### 查看所有打开的网络端口及使用该端口的程序
```
$ ss -pl
p_dgr  UNCONN     0      0                                                                  arp:br0                                                                                 *                      users:(("NetworkManager",pid=1108,fd=18))
u_str  LISTEN     0      10                                           /var/run/abrt/abrt.socket 22795                                                                              * 0                     users:(("abrtd",pid=996,fd=9))
u_str  LISTEN     0      5                                                 /var/run/lsm/ipc/sim 22547                                                                              * 0                     users:(("lsmd",pid=977,fd=4))
u_dgr  UNCONN     0      0                                                  /run/systemd/notify 276                                                                                * 0                     users:(("systemd",pid=1,fd=23))
u_dgr  UNCONN     0      0                                           /run/systemd/cgroups-agent 278                                                                                * 0                     users:(("systemd",pid=1,fd=24))
u_str  LISTEN     0      128                                        /run/systemd/journal/stdout 286                                                                                * 0                     users:(("systemd-journal",pid=620,fd=3),("systemd",pid=1,fd=28))
```

#### 查看所有的TCP Sockets
```
$ ss -t -a
State      Recv-Q Send-Q                                                      Local Address:Port                                                                       Peer Address:Port                
LISTEN     0      10                                                              127.0.0.1:smtp                                                                                  *:*                    
LISTEN     0      128                                                                     *:sunrpc                                                                                *:*                    
LISTEN     0      5                                                           192.168.122.1:domain                                                                                *:*                    
LISTEN     0      128                                                                     *:ssh                                                                                   *:*                    
ESTAB      0      0                                                             17.16.3.129:ssh                                                                           17.16.3.1:49353                
ESTAB      0      0                                                             17.16.3.129:ssh                                                                           17.16.3.1:50507                
LISTEN     0      128                                                                    :::terabase                                                                             :::*                    
LISTEN     0      128                                                                    :::sunrpc                                                                               :::*                    
LISTEN     0      128                                                                    :::35729                                                                                :::*                    
LISTEN     0      128                                                                    :::ssh                                                                                  :::*                    
ESTAB      0      0                                                      ::ffff:17.16.3.129:35729                                                                  ::ffff:17.16.3.1:55024      
```

#### 查看所有已经建立的ssh连接 
```
$ ss -o state established '( dport = :ssh or sport = :ssh )'
Netid  Recv-Q Send-Q                                                        Local Address:Port                                                                         Peer Address:Port                
tcp    0      0                                                               17.16.3.129:ssh                                                                             17.16.3.1:49353                 timer:(keepalive,87min,0)
tcp    0      0                                                               17.16.3.129:ssh                                                                             17.16.3.1:50507                 timer:(keepalive,19min,0)
```

#### 根据状态过滤Sockets
> 格式：
> ss state FILTER-NAME-HERE  
FILTER-NAME-HERE可选：established、syn-sent、syn-recv、fin-wait-1、fin-wait-2、time-wait、closed、close-wait、last-ack、listen、closing  
all：包含以上所有状态  
connected：除了listen和closed的所有状态  
synchronized：除了syn-sent之外的所有已连接的状态  
bucket：显示状态为maintained as minisockets，如time-wait和syn-recv  
big：和bucket相反

```
$ ss -4 state established
Netid  Recv-Q Send-Q                                                        Local Address:Port                                                                         Peer Address:Port                
tcp    0      236                                                             17.16.3.129:ssh                                                                             17.16.3.1:49353                
tcp    0      0                                                               17.16.3.129:ssh                                                                             17.16.3.1:50507                
```

### 匹配本地地址和端口号
>格式： ss src ADDRESS_PATTERN

```
$ ss src 17.16.3.129
Netid  State      Recv-Q Send-Q                                                   Local Address:Port                                                                    Peer Address:Port                
tcp    ESTAB      0      244                                                        17.16.3.129:ssh                                                                        17.16.3.1:49353                
tcp    ESTAB      0      0                                                          17.16.3.129:ssh                                                                        17.16.3.1:50507                
tcp    ESTAB      0      0                                                   ::ffff:17.16.3.129:35729                                                               ::ffff:17.16.3.1:54615               
```
