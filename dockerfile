FROM harbor.finupgroup.com/basic/python3:latest

COPY *.py /root/

COPY weixin /root/weixin

WORKDIR /root

EXPOSE 8004

CMD ["python", "main.py"]

