# -*- coding: utf-8 -*-

import inspect
import os
import re

HOST = 'https://fishpi.cn'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'

HELP = '输入#help获得命令提示列表'

COMMAND_GUIDE = '''
[#cli] 进入命令交互模式
[#cr] 进入聊天室模式
[#chat] 私聊 #chat Gakkiyomi 进入和Gakkiyomi的私聊窗口
[#siguo] 思过崖
[#article] 看帖 (默认显示20个帖子) [view|page] (int) / 回帖 #article comment (str)
[#rp] 1 128 1个128积分 (默认5个,128积分)拼手气红包
[#rp-ave] 1 128 1个128积分 (默认5个,32积分)平均红包
[#rp-hb] 5 128 5个128积分 (默认5个,32积分)心跳红包
[#rp-rps] 0 128 128积分 (0=石头 1=剪刀 2=布)猜拳红包
[#rp-rps-limit] 100 (猜拳红包超过100的不抢)
[#rp-to] 32 Gakkiyomi,xiaoIce (积分 用户)专属红包
[#rp-time] 3 设置抢红包等待时间
[#bm] 发送清风明月
[#config] 查看,导出配置文件 config [dump|show] {-d|-c} (file_path)
[#answer] 进入|退出 答题模式
[#checked] 查看当前是否签到
[#reward] 领取昨日活跃奖励
[#revoke] 撤回最近一条聊天室消息
[#transfer] 32 Gakkiyomi 送给你 (积分 用户 留言)
[#point] 查看当前个人积分
[#online-users] 查看当前在线的用户列表
[#user username] 输入 #user 用户名 可查看此用户详细信息 (#user Gakkiyomi)
[#me] 查看当前在线账号 #me (-d) 查看账户详情 #me article (view | page){index} 查看自己的帖子
[#push] 推送帖子 #push article {index} 文章索引号
[#account] 查看分身账号
[#su] 账号切换 #su Gakkiyomi
[#bl] 查看黑名单列表
[#op-mode] 设置窗口输出模式 op-mode {file|backup|console} 支持控制台输出,文件输出,备份输出模式
[#op-path] 设置输出路径文件 op-path /abc/chatroom.log
[#ban keyword|user xxx] 将某人或者关键词送入黑名单
[#release keyword|user xxx] 将某人或者关键词解除黑名单
[#notification {-d|-a}}] keyword 动态修改关键词提醒
[#liveness] 查看当前活跃度(⚠️慎用，如果频繁请求此命令(最少间隔30s)，登录状态会被直接注销,需要重启脚本！)
'''

RPS_SUCCESS = '![](https://file.fishpi.cn/2023/01/XN3Y9-cf3997b7.jpeg)'
RPS_LOSED = '![](https://pwl.stackoverflow.wiki/2022/04/MB2SCYFZFVT2DQ0GI7-c6447c10.jpg)'
RPS_ZERO = '![](https://file.fishpi.cn/2023/05/1683183148506-4c31497e.png)'


RP_RE = re.compile(r'(\d) (\d+)')
RP_SEND_TO_CODE_RE = re.compile(r'(\d+) ([\w,]+)(?<!,)$')
RP_TIME_CODE_RE = re.compile(r'(\d+)')
TRANSFER_RE = re.compile(r'(\d+) (\w+)( \S+)?')
OUTPUT_RE = re.compile(r'(file|backup|console)')
HOST_RE = re.compile(r'^https?://')


def cli_login(cli_user: str) -> bool:
    env_user = os.environ.get('FISH_PI_USERNAME', '')
    return env_user != cli_user
