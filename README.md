# Python-Django-天天生鲜项目

功能:用户注册，用户登录，购物车，用户中心，首页，订单系统，地址信息管理，商品列表，商品详情，支付功能等等，是一个完整的电商项目流程


## 技术栈
python + django + mysql + redis + celery + FastDFS(分布式图片服务器) + nginx


## 目标功能:
- [x] 功能模块
    - [x] 用户模块
        - [x] 注册
        - [x] 登录
        - [x] 激活(celery)
        - [x] 退出
        - [x] 个人中心
        - [x] 地址管理
    - [x] 商品模块
        - [x] 首页(celery)
        - [x] 商品详情
        - [x] 商品列表
        - [x] 搜索功能(haystack+whoose)
    - [x] 购物车模块(redis)
        - [x] 增加
        - [x] 删除
        - [x] 修改
        - [x] 查询
    - [x] 订单模块
        - [x] 确认订单页面
        - [x] 订单创建
        - [x] 请求支付(支付宝)
        - [x] 查询支付结果
        - [x] 评论
        
        
## FastDFS
[安装教程](https://wangxin1248.github.io/linux/2020/03/ubuntu-install-fastdfs.html#top)

[故障处理](https://www.jianshu.com/p/de789d6ea126)
## celery
```shell script
python3 -m  celery -A  tasks worker -l info
```
