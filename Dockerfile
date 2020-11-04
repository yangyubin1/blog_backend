FROM yyb_blog:v1.0
WORKDIR /data
#ARG TZ="Asia/Shanghai"
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
#        && echo $TZ > /etc/timezone
COPY . /data
#CMD ["python","-u","/data/manage.py runserver 0.0.0.0:9090"]
RUN cd /data
RUN sed -i 's/\r//' ./start.sh
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
CMD ["sh","-c","./start.sh"]

