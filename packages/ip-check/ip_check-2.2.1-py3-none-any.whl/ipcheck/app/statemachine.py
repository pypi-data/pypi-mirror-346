#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from ipcheck.app.utils import singleton
from ipcheck.app.ip_info import IpInfo
from ipcheck import WorkMode

# 工具类，存储一些运行时全局数据

@singleton
class StateMachine:

    def __init__(self) -> None:
        self.ip_list = []
        self.geo_loc_avaiable = False
        self.geo_asn_org_avaiable = False
        self.work_mode = WorkMode.DEFAULT

    @classmethod
    def clear(cls):
        self = cls()
        self.ip_list.clear()

    @classmethod
    def cache(cls, ipinfo: IpInfo):
        self = cls()
        self.ip_list.append(ipinfo)

    @classmethod
    def print_cache(cls):
        self = cls()
        fixed_ip_list = []
        if self.ip_list:
            fixed_ip_list = sorted(self.ip_list, key=lambda x: (x.max_speed * -1, x.rtt, x.country_city))
            print('当前测试阶段IP 信息如下:')
            for ip_info in fixed_ip_list:
                print(ip_info)