import argparse
from host.gethost import *

def get_para():
    parser = argparse.ArgumentParser(description='Domain Name System')

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", action="store_true", help="Level-1 Debuging")
    group.add_argument("-dd", action="store_true", help="Level-2 Debuging")

    parser.add_argument("-a","--addr", help="DNS server IP address", type=str)
    parser.add_argument("-f","--file", help="Default hostfile: \"dnsrelay.txt\"", type=str)
    args = parser.parse_args()

    return args

""" 
    debug_level
    0：无输出
    1：仅输出时间坐标，序号，客户端IP地址，查询的域名
    2：输出冗长的调试信息
    host:处理好的对照表
    address:远程DNS服务器
"""
def Handle_para(args, default):

    if not (args.d or args.dd):
        print("No debug-information output.")
        mode = 0
    elif args.d:
        print("Level-1 debug-information output")
        mode = 1
    elif args.dd:
        print("Level-2 debug-information output")
        mode = 2

    if args.addr is None:
        print("Use default remote DNS server address\t:" , default.address)
        addr = default.address
    else:
        print("Use user's DNS server address\t\t\t:" , args.addr)
        addr = args.addr
    
    if args.file is None:
        print("Use default hostfile\t\t\t:" , default.hostfile)
        hosts = gethost(default.hostfile)
    else:
        print("Use user's hostfile\t\t\t:" , args.file)
        hosts = gethost(args.file)

    return dict(mode = mode, hosts = hosts, addr = addr)
        


