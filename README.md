# MuMuYYS

一款图像识别+鼠标点击的示例

## 打包 exe

```bash
pyinstaller -F main.py
````

## 一键打包(使用 bandizip 压缩)

```bash
python package.py
```

## 导出配置

```bash
pip freeze > requirements.txt
```

## 环境安装

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```