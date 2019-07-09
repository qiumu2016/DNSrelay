from util.parameters import *
from settings.settings import Settings
from serve.server import DNSServer
if __name__ == "__main__":
    #处理默认设置
    default_settings = Settings()
    #处理命令行参数
    args = get_para()
    #合成运行参数
    startInfo = Handle_para(args, default_settings)
    #实例化服务对象
    dnsServer = DNSServer(default_settings, startInfo)
    #启动服务
    dnsServer.start()


    