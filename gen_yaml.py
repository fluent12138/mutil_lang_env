import argparse
import yaml

# 创建一个 ArgumentParser 对象
parser = argparse.ArgumentParser(description='Generate a docker-compose.yaml file.')

# 添加参数
parser.add_argument('-lang', '--language', type=str, required=True, help='缺少编程语言信息')
parser.add_argument('-name', '--service_name', type=str, required=True, help='缺少服务名称信息')
parser.add_argument('-image', '--image', type=str, required=True, help='缺少Docker镜像信息')
# 个人理解为可以把宿主机的文件映射到docker容器中, 这样修改宿主机的文件, 就可以在docker容器中编译运行了
parser.add_argument('-from_dir', '--from_dir', type=str, required=True, help='缺少挂载的文件目录信息')
parser.add_argument('-to_dir', '--to_dir', type=str, default='/lang', help='缺少docker容器的文件目录信息')
parser.add_argument('-p', '--port', type=str, action='append')
parser.add_argument('-env', '--env', type=str)
# 解析命令行参数
args = parser.parse_args()

# 语言到环境变量的映射
language_to_env = {
    'go': 'GOPATH',
    # 可以根据需要添加更多语言映射
}

# 获取对应语言的环境变量名
env_name = language_to_env.get(args.language)

# 如果语言不支持，则提醒
if env_name is None:
    print(f"!!! 未支持{args.language}环境变量映射, 你可以选择忽略或添加{args.language}配置 !!!")

# 设置默认端口为8080，如果port参数未提供
if not args.port:
    args.port = ['8080']

# 创建服务配置
services = {
    args.service_name: {
        'image': args.image,
        'environment': [
            f'{env_name}={args.env}'
        ],
        'volumes': [
            f'{args.from_dir}:{args.to_dir}'
        ],
        'working_dir': args.to_dir,
        # 映射所有指定的端口
        'ports': [f'{p}:{p}' for p in args.port],
        # 使得docker容器可以挂起 不会退出, 也许你有更好的方法, 那请果断干掉这个语句, 因为作者对docker-compose并不熟悉
        'command': 'tail -f /dev/null'
    }
}

# 创建 docker-compose 配置
docker_compose = {
    'version': '3',
    'services': services
}

# 生成 docker-compose.yaml 文件
with open('docker-compose.yaml', 'w') as file:
    yaml.dump(docker_compose, file, default_flow_style=False)

# 打印docker-compose.yaml内容
with open('docker-compose.yaml', 'r') as file:
    print("======== 已成功生成docker-compose.yaml文件 ======== \n", file.read())
