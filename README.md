# chat_robot

## 开发环境

```bash
# 创建虚拟环境
pip install virtualenv
virtualenv venv --no-site-packages
```

```bash
# 进入虚拟环境安装依赖
source venv/bin/activate
pip install -r requirements
```

```bash
# 目前 instance 里的 config.py 仅供测试
python manage.py init

# 如果需要添加少量测试数据的话
# python manage.py test

# 运行
python run.py
```