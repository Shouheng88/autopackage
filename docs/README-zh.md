# Android 自动打包脚本

[English](README.md)

## 1. 关于

该项目是适用于 Android 的自动打包脚本，主要功能：

- 使用 gradle 指令自动打包，区分 32 位和 64 位
- 打包完成之后将 APK 拷贝到指定的目录
- 使用 [diffuse](https://github.com/JakeWharton/diffuse) 输出相对于上一个版本的 APK 版本差异报告
- 拷贝多语言资源到指定的目录，并自动提交到 Github 仓库以便于协助翻译
- 自动打 tag 并提交到远程仓库
- 根据 Git 提交记录自动生成更新日志
- 使用 [360 加固](https://jiagu.360.cn/#/global/index) 对上述 APK 进行加固并输出到指定的目录
- 基于 [VasDolly](https://github.com/Tencent/VasDolly) 进行多渠道打包
- 上传打包 APK 到蓝奏云
- 通过 Telegram bot 将打包完成的渠道包和更新日志信息发送到 Telegram 群组
- 完成上述操作之后使用邮件通知打包结果
- 未来，更多功能...

## 2. 使用

### 2.1 环境

- Python: Python3
- 添加 `pyymal` 库: `pip install pyyaml`
- 添加 `requests` 库: `pip install requests`
- 添加 `requests_toolbelt` 库: `pip install requests_toolbelt`

### 2.2 使用

- 编辑配置文件 [the configuration file](config.yml)
- 在根目录使用 `python run.py` 执行脚本
