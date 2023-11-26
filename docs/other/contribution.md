# Contribution

如果你想要参与贡献，你可以先查看[当前开发计划](other/plan.md)，查看你想开发的功能是否正在开发中，如果你想要开发新的功能，欢迎你在issue中提出相关的想法。

## 本地开发

**环境要求**
- Python >= 3.8
- make

> 本项目使用 make 进行项目配套设施的构建，通过 makefile 的能力轻松集成运行 test、lint 等模块，请确保你的电脑已经安装了 make。
> 
> [how to install and use make in windows?](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows)


运行以下命令：

```shell
git clone https://github.com/Undertone0809/promptulate 
```

下载到本地之后，安装第三方库

```shell
pip install poetry
make install
```


本项目使用配备代码语法检查工具，如果你想提交 pr，则需要在 commit 之前运行 `make polish-codestyle` 进行代码规范格式化，并且运行 `make lint` 通过语法与单元测试的检查。