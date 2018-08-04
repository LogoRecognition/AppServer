# AppServer

## How to install
```bash
# 安装虚拟环境virtualenv
pip install virtualenv
# 克隆仓库
git clone https://github.com/LogoRecognition/AppServer
# 切换到项目源码目录
cd AppServer/server
# 新建虚拟环境并指定Python版本
virtualenv venv -p python3
# 激活虚拟环境
source venv/bin/activate
# 安装第三方模块
pip install -r requirements.txt
```

## How to run
运行项目前，需要在`server`目录下新建`instance`目录，并在`instance`目录下新建`config.py`文件，在`config.py`中添加项目的私密配置，例如：

```python
DB_USERNAME = 'username'      	# MySQL用户名
DB_PASSWORD = 'password'      	# MySQL密码
DB_NAME = 'logo'             	# 数据库名称
SECRET_KEY = 'HELLO'            # 会话秘钥
IMAGE_FOLDER = '../images/'		# 图片目录
```

然后切换至`server`目录下：

```bash
# 自动添加数据
python scripts/add_brands.py
# 运行服务器程序
python run.py
```
