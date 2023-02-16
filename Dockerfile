FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用程序代码到镜像中
COPY . /app

# 安装依赖项
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install vim -y \
    && pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

#使用 ENTRYPOINT 命令来指定一个启动脚本，然后在脚本中执行命令
ENTRYPOINT ["/bin/bash", "-c"]
# 设置启动命令
CMD ["flask run -h 0.0.0.0 -p 8000 >> ../log"]