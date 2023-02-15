FROM python:3.9-slim

# 设置工作目录
WORKDIR /openAI

# 复制应用程序代码到镜像中
COPY . /openAI

# 安装依赖项
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install vim -y \
    && pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD [ "python", "ChatApi.py" ]