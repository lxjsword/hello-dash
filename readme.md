# 使用说明

## 配置.env文件
SECRET_KEY=xxxxxx
DASH_ENV=dev

## 启动
### 测试环境
python app.py

### 正式环境
gunicorn -c gunicorn.conf app:server


## 常用命令
### 初始化数据库
flask my_command initdb
flask my_command initdb --drop

### 新增用户
flask my_command create_user

### 重置密码
flask my_command reset_passwd