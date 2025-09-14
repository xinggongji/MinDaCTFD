# HOW to 搭建一个CTF靶场

## 介绍
#### 手把手教你搭建一个属于你的CTF靶场

## 前置
#### 需要一个有docker服务的环境（本示范以装有服务的Ubuntu为例子 后文简称为环境机）


## 具体安装教程

#### 1.  查询环境机的ip （本示范例为192.168.147.132 后续请自行将ip更换）
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-19%20211637.png)
#### 2.  将安装包在环境机git clone 或 下载后添加到环境机中

```
git clone https://gitee.com/xinggongji/min-da-ctfd.git
```

```
scp -r 本机文件下载地址 环境机用户@环境机ip:~
```


#### 3.  解压并在文件所在目录进入终端后输入

```
docker swarm init
```

```
docker node update --label-add='name=linux-1' $(docker node ls -q)
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-19%20213301.png)
#### 4.  启动docker容器 等待一段时间(约几分钟)并看到五个容器全部成功启动

```
docker-compose up -d
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-21%20124301.png)
#### 5. 访问环境机ip的80端口即可看到CFTD靶场
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-19%20214812.png)
## 动态靶机配置

#### 1.  进入目录Frp-Docker-For-CTFd-Whale-double并输入（第一条命令如果第一次启动会warning容器未找到 直接忽略就好）

```
docker-compose down
```

```
docker-compose up -d
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-21%20154720.png)
#### 2.  在靶场管理面板的whale--路由 并按照下图修改（ip地址记得换）
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-21%20155018.png)
#### 3. 退回到min-da-ctfd目录 并进入frp目录 修改frpc.ini中的serve-addr为环境机ip 并将内容复制到靶场管理面板的whale--路由

```
vim frpc.ini
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235056.png)
#### 4. 再进入目录Frp-Docker-For-CTFd-Whale-double 并进入frp目录 将frps.ini中内容改为下图位置中内容

```
cat frps.ini
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235125.png)

#### 5. 退回到min-da-ctfd目录 查看重启容器min-da-ctfd_frpc_1 并将该容器名字复制到下图位置（管理面板--whale--docker）

```
docker restart min-da-ctfd_frpc_1
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235552.png)
#### 6. `docker network ls` 查看并复制标注内容到图2位置 
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235632.png)
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235703.png)
#### 7.  `systemctl status docker` 将标注目录中文件 **以管理员权限** 改写（其原内容为fd://）为图2所示 （端口号可以自拟 不冲突即可）
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235850.png)

```
sudo vim /lib/systemd/system/docker.service
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-21%20000146.png)

```
unix:///var/run/docker.sock -H tcp://192.168.147.132:2365
```
#### 8. 重启docker （可能稍慢需等待一会

```
systemctl daemon-reload
```

```
systemctl restart docker
```
#### 9. 最后将api URL更换为环境机ip加端口
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-21%20000506.png)
