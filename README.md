# box4399_assistant

#### 介绍
- 自用的4399游戏盒签到库，可以满足简单的自动签到和抢奖品功能。
- 仓库内容比较混乱，稍后会进行整理。

#### 软件架构
Python为主

#### 仓库结构介绍
##### python-mainstream folder
- 包含了可以正常使用的python脚本
- 包含以下功能：
    - 自动获取积分
    - 监控加速卡补仓状态
    - 自动抢加速卡并签到
    - 自动补签+签到当天
    - 自动抢每月奖励

##### 易语言 folder
- 包含了exe格式的脚本文件，功能更加完善
- 包含以下功能：
    - 封包分析功能
    - 自动获取积分(快速版)
    - 监控加速卡补仓状态
    - 自动抢加速卡
    - 自动签到
    - 一键补签
    - 签到状态查询
    - 自动抢奖品(限量及不限量)
    - 奖品状态一键转换
    - 切换签到的游戏
    - 提前输入验证码功能
    - 提前绑定游戏账号
- Warning：
    - 为了防止脚本扩散及转卖，在程序中对部分功能添加了二次验证。如需解锁全部功能，请在Bilibili私信[In-Dream](https://space.bilibili.com/438249457)您的电脑机器码。
    - 程序使用易语言编写，可能会出现报毒，请谨慎使用

##### python-async folder
- 包含了使用协程重构的python脚本，发包速率更快，但是功能不全面
- 目前实现的功能有限，包括：
    - 监控加速卡补仓状态
    - 自动抢奖品(限量及不限量)
- 不推荐使用

##### python-server folder
- 包含了django框架下的、集成在微信公众号内的功能模组
- 可以挂载在服务器上24小时运行，也可以进行二次开发添加更多功能
- 目前实现的功能如下：
    - 监控加速卡补仓状态(可以通过访问[4399box/acc_rd](http://47.93.116.121/4399box/acc_rd)查询)
    - 设置游戏id
    - 解析封包
    - 签到状态查询
    - 自动获取积分(每天零点自动执行)
    - 提前填写验证码功能(可以通过访问[4399box/verify?id=微信id](http://47.93.116.121/4399box/verify?id=xxx)进行)
    - 权限限制(可以指定白名单中的用户使用功能)
- 请谨慎使用该功能

##### javascript folder
- 包含了一些测试性的js发包代码
- 使用了ajax作为发包工具，发包速率巨快
- 里面实现了一份利用ajax来快速发包抢限量礼包的代码
- 存在的问题：
    - 无法修改User-Agent,因此容易被服务器拦截
    - 没有对账号可行性进行验证

#### 联系方式
如果仓库内容出现侵权，请在Bilibili私信[In-Dream](https://space.bilibili.com/438249457)。