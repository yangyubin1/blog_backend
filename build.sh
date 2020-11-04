#!/bin/sh

#if [[ -z ${MODEL} ]]; then
#      echo envirenment 'MODEL' is empty
#        exit 1
#    fi

#cd ./codes/
#sed -i "s/huanjingbianliang/${MODEL}/" config.py

#cd ..
docker rm -f yyb_blog
docker rmi  vue_blog_image:v1.0
docker build -t vue_blog_image:v1.0 . < Dockerfile
#docker tag hoc/drone-jenkins docker.io/hoc/drone-jenkins
docker rm -f yyb_blog
docker run -d \
     -e PLUGIN_APPNAME=aceqry01 \
     -p 9090:9090 \
     --name=yyb_blog  \
     -v /root/item/python_item/vue_blog_backend:/data \
     -v /etc/localtime:/etc/localtime \
     --restart unless-stopped \
   vue_blog_image:v1.0


#docker run hoc/drone-aop drone-jenkins # -host http://192.168.16.77:8080/ -user dianpeng-zhou -token 114e44c6dc3e9c6ad271adb053d4c78422 -job testss
