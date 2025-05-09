# Cookiecutter-seatools-python-codegen

Cookiecutter-seatools-python 代码生成拓展包 uv 分支

## 仓库地址:

1. https://github.com/seatools-py/cookiecutter-seatools-python-codegen
2. https://gitee.com/seatools-py/cookiecutter-seatools-python-codegen

## Cookiecutter-seatools-python 模板项目地址

1. https://github.com/seatools-py/cookiecutter-seatools-python
2. https://gitee.com/seatools-py/cookiecutter-seatools-python

## Seatools 工具包地址

1. https://github.com/seatools-py/seatools
2. https://gitee.com/seatools-py/seatools

## 安装

安装命令: `uv add scodegen`
windows工具 `scodegen.exe`, linux工具 `scodegen`

## 使用示例 （以windows工具为例）

- 创建新应用

```shell
# 创建一个新应用, 单应用项目无需使用, cookiecutter-seatools-python 项目模板自带一个默认的主应用包
scodegen.exe startapp [应用名称]
# 示例
scodegen.exe startapp xxx
# 查看命令帮助
scodegen.exe startapp --help
```

- 创建一个CMD工具

```shell
# 创建一个CMD, 使用 cookiecutter-seatools-python 主项目包时无需配置--app, 使用新建应用需要传递该值
scodegen.exe cmd --name [命令名称]
# 示例
scodegen.exe cmd --name xxx
# uv 运行
uv run xxx
# linux运行
bash bin/xxx.sh
```

- 创建一个任务

```shell
# 创建一个任务
scodegen.exe task --class xxx_task --name Xxx任务
# 创建异步任务
scodegen.exe task --class async_xxx_task --name Xxx异步任务 --async
# 创建带cmd的任务
scodegen.exe task --class xxx_task --name XXX任务 --cmd
# uv运行
uv run xxx_task
# linux运行
bash bin/xxx_task.sh
```

- 生成FastAPI项目

```shell
# 生成FastAPI模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
scodegen.exe fastapi
# 安装依赖
uv add fastapi uvicorn[standard]
# uv运行
uv run fastapi
# linux运行
bash bin/fastapi.sh
```

- 生成Flask项目

```shell
# 生成Flask模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
scodegen.exe fastapi
# 安装依赖
uv add flask uvicorn[standard]
# uv运行
uv run flask
# linux运行
bash bin/flask.sh
```

- 生成Django项目

```shell
# 生成Django模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
scodegen.exe django
# 安装依赖
uv add django uvicorn[standard]
# uv运行
uv run django_runserver
# linux运行
bash bin/django.sh
```

- 生成Scrapy项目

```shell
# 生成Django模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
scodegen.exe scrapy init
# 生成Scrapy爬虫
scodegen.exe scrapy genspider xxx xxx.com
# uv运行爬虫
uv run xxx
# linux运行爬虫
uv run xxx
```
