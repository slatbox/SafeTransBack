# 简易安全传输系统

## 项目结构

+ download：下载文件目录
+ keys：CA，服务端，以及用户端的证书及密钥
+ storage：服务端的文件存储区
+ client.py：用户端接口
+ database.py：sqlite3数据库接口
+ frontend.py：用户端前端程序
+ protocal：协议封装接口
+ server.py：服务端程序

## 技术路线

+ 基于python实现
+ GUI使用PySimpleGUI实现
+ 数据库使用sqlite3轻量级数据库

## 核心功能实现方法

+ 使用threading模块实现多用户并发访问
+ 使用ssl+socket模块实现安全的文件传输可抵御中间人攻击
+ 使用sqlite3数据库预编译功能，抵御SQL注入攻击
+ 使用加盐hash的方法可以抵御脱库等攻击

## 运行方法

### 安装相关依赖

```bash
pip3 install PySimpleGUI
```

### 运行

```bash
# 运行服务器
python3 server.py

# 运行客户端程序
pyhton3 frontend.py
```
