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
# 若library/db.sqlite 存在则无需初始化数据库
# python manage.py init

# 运行
python run.py
```