class Settings():
    """存储DNSrelay的所有默认设置"""
    def __init__(self):
        '''默认端口号'''
        self.port = 53
        '''默认远程DNS服务器地址'''
        self.address = "10.3.9.4"
        '''默认名字对照文件'''
        self.hostfile = "dnsrelay.txt"
