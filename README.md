# Auto Package

## 1. What?

An Android auto package script. Mainly used to 

- Call gradlew command to package APKs, 32 bit and 64 bit separately 
- Copy APKs to given directory
- Diff APK with last version or output its info base on [diffuse](https://github.com/JakeWharton/diffuse)
- Copy language resources to given dirctory, commit to github repo for translation cooperation
- Add git tag automatically and push to remote git repo
- Automatically generate APP upgrade log from git logs
- Reinforce APKs by [360 Security](https://jiagu.360.cn/#/global/index)
- Notify receivers when succeed by email
- More in the future.

## 2. How?

### 2.1 Prepare

- Python: Python3
- Add `pyymal` library to your environment by: `pip install pyyaml`

### 2.2 Use

- Configure [the configuration file](config.yml).
- Execute `python run.py` under root directory.
