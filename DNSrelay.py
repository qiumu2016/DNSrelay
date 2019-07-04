from util.para import *
from host.gethost import gethost
from settings.settings import Settings
from serve.server import DNSServer
if __name__ == "__main__":
    default_settings = Settings()
    args = get_para()
    #print(args)
    startInfo = Handle_para(args, default_settings)
    #print(startInfo)
    dnsServer = DNSServer(default_settings, startInfo)
    dnsServer.start()


    