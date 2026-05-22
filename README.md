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
#### 5. 进行数据库更新新增字段防止报错

```
docker-compose exec ctfd flask db migrate -m "add new fields"
```



```
docker-compose exec ctfd flask db upgrade
```


#### 6. 访问环境机ip的80端口即可看到CFTD靶场
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
#### 3. 退回到min-da-ctfd目录 并进入frp目录 修改frpc.ini中的serve-addr为环境机ip 并将内容复制到靶场管理面板的whale--路由 之后点击提交下方出现生成模版

```
vim frpc.ini
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235056.png)
#### 4. 再进入目录Frp-Docker-For-CTFd-Whale-double 并进入frp目录 将frps.ini中内容改为下图位置中内容

```
cat frps.ini
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235125.png)

#### 5. 退回到min-da-ctfd目录 重启容器min-da-ctfd_frpc_1（只需要重启这一个容器） 并将该容器名字复制到下图位置（管理面板--whale--docker）

```
docker restart min-da-ctfd_frpc_1
```
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235552.png)
#### 6. `docker network ls` 查看并复制标注内容`min-da-ctfd_frp_containers`到图2位置 
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235632.png)
![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-05-20%20235703.png)
最后点击提交即可


# CTF web 出题/上题文档

## 参考链接

[如何用 docker 出一道 ctf 题 (web) | 枫霜月雨の blog](https://liuxin2020.github.io/2021/09/28/%E5%A6%82%E4%BD%95%E7%94%A8docker%E5%87%BA%E4%B8%80%E9%81%93ctf%E9%A2%98(web)/)

[https://blog.csdn.net/Elite__zhb/article/details/134472115](https://blog.csdn.net/Elite__zhb/article/details/134472115)

ctf出题模板地址：[https://github.com/CTF-Archives/ctf-docker-template](https://github.com/CTF-Archives/ctf-docker-template)

## 出题指南

CTFD平台在装载whale插件后可以实现动态flag。其原理是开启靶机后，系统从打包好的镜像加载容器，并且把随机的flag参数注入容器的`$FLAG`环境变量中。

**php环境输出flag示例**

```sql
<?php
echo "webtest";
echo $_ENV['FLAG'];
?>
```

**python环境输出flag示例**

```sql
flag_value = os.getenv('FLAG')
return flag_value
```

还可以通过启动脚本把flag写入数据库、或者指定路径的文件中，详细请参考出题模板：

[https://github.com/CTF-Archives/ctf-docker-template](https://github.com/CTF-Archives/ctf-docker-template)

## 上题流程

1、进入题目目录下，在Dockerfile同级目录下编译镜像

```sql
cd webtest
#注意！在-t参数后还要空格加上一个点 . 表示在本目录下！！！
docker build -t webtest:latest .
#查看编译好的镜像
docker images
```

2、进入CTFD管理后台的Challenges页面，点击上方加号新建题目，选择**dynamic_docker**，填写好相关信息

![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%87%BA%E9%A2%981.png)

3、重点关注以下三个信息

**Docker Image** 填入第 1 步docker build -t 参数 后自定义的镜像名字

**Frp Redirect Type** 选择 Direct

**Frp Redirect Port** 填入Dockerfile 暴露的对应端口，一般是80端口

![输入图片说明](read%E5%9B%BE%E7%89%87/%E5%87%BA%E9%A2%982.png)

填入好以上必要信息后即可创建web题目，完成出题流程

## 常见问题汇总

### 学校服务器无法build镜像？

在本文档制作时，学校服务器由于不可抗力因素无法直接build镜像，可以现在自己的环境上将镜像构建好再打包过去。

```sql
#本地服务器
cd webtest
docker build -t webtest:latest .
docker images
docker save -o webtest.tar webtest:latest
```

利用ssh将打包好的tar包传到学校服务器上后，执行以下命令，即可在本地加载镜像

```sql
#学校服务器
docker load -i webtest.tar
```