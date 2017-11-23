#!/bin/sh  

# Shell 开启博客 命令

#

# 开启资源服务器
cd StaticServer/
python3 -m SimpleTornadoServer 8081 &

#开启blog服务器
cd ../blog
python3 manage.py runserver 0.0.0.0:5000 &


