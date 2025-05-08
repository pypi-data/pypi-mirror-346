#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__createTime__ = "2025/5/8 09:47"
__author__ = "WeiYanfeng"
__email__ = "weber.juche@gmail.com"
__version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述

封装 CNameValueCsv 类，从 name=value # remarks 格式文本读取配置参数
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from .WyfPublicFuncs import PrintTimeMsg
from .PrettyPrint import PrettyPrintStr
# from weberFuncs import PrintTimeMsg, PrettyPrintStr


def load_name_value_dict(sFullFN):
    # 从 name=value # remarks 格式文本读取配置参数
    dictConfig = {}
    try:
        with open(sFullFN, 'r', encoding='utf8') as f:
            for sLine in f:
                sLine = sLine.strip()
                if not sLine or sLine.startswith('#') or ('=' not in sLine):
                    # 空串没有等号，则是不正常的key=value配置，直接忽略
                    continue
                sKey, cSep, sValue = sLine.partition('=')
                if '#' in sValue:  # 剔除行内注释
                    sV, cSep, sC = sValue.partition('#')
                    sValue = sV
                sKey = sKey.strip()
                sValue = sValue.strip('\'\" \t')  # 删除引号及空白
                if sKey:
                    dictConfig[sKey] = sValue
    except Exception as e:
        PrintTimeMsg(f'load_name_value_dict({sFullFN}).e={repr(e)}=')
    PrintTimeMsg(f'load_name_value_dict.dictConfig={PrettyPrintStr(dictConfig)}=')
    return dictConfig


def main():
    sFN = r'E:\WeberSrcRoot\Rocky9GogsRoot\RobotAgentMCP\TaskMcpClient\mcp.server\cmdPath.env'
    load_name_value_dict(sFN)


# --------------------------------------
if __name__ == '__main__':
    main()
