# Auto Package

An Android auto package script. Mainly used to 

- Call gradlew command to package APKs
- Copy APKs to given directory
- Diff APK with last version or output its info base on [diffuse](https://github.com/JakeWharton/diffuse)
- Copy language resources to given dirctory, commit to github repo for translation cooperation
- Add git tag automatically and push to remote git repo
- More in the future.

## Prapare

- Python: Python3
- Add `pyymal` library to your environment by: `pip install pyyaml`

## Usages

- Configure [the configuration file](config.yml).
- Execute `python run.py` under root directory.
