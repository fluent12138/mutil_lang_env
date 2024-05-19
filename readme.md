# 多语言环境搭建

### 目录结构

```
.
|-- README.md
|-- docker-compose.yaml
|-- gen_yaml.py
```

### 使用说明

1. 确保您的系统中已安装 Docker 和 Docker Compose。
2. 运行 `gen_yaml.py` 脚本来生成 `docker-compose.yaml` 文件。
3. 使用 `docker-compose up -d` 命令启动服务。
4. 如果您需要进入容器并使用 `bash`，可以使用`docker-compose exec name bash` 命令。
5. 使用 `docker-compose down` 命令停止并删除容器和网络。

### 生成 Docker Compose 配置

- 以生成go环境配置为例

- ```python
    # 使用命令生成docke-compose.yaml文件
    # -lang 为对应语言参数
    # -name 为启动服务名称
    # -image 为对应docker镜像
    # -from_dir 为宿主机文件夹路径
    # -to_dir 映射到docker容器的文件夹路径
    # -env 环境变量, 可以按需要添加
    # -p 映射端口号
    python3 gen_yaml.py -lang go -name go -image golang:1.17 -from_dir /root/gops/ -to_dir /go -env /go -p 9000 -p 9001
    ```

- ```yaml
    # 生成docker-compose.yaml文件如下
    services:
      go:
        command: tail -f /dev/null
        environment:
        - GOPATH=/go
        image: golang:1.17
        ports:
        - 9000:9000
        - 9001:9001
        volumes:
        - /root/gops/:/go
        working_dir: /go
    version: '3'
    ```

### 启动服务

```shell
# 启动docker服务
docker-compose up -d
```

### 进入容器并执行对应命令

```shell
# 进入容器内部 name即为对应docker服务名称
docker-compose exec name bash
# go环境
go run file
# java环境
javac file
java file
# erlang环境
erl
# ... ...
```

### 停止并删除服务

```shell
# 关闭docker服务
docker-compose down
```

