from util.para import *
from host.gethost import gethost
from settings.settings import Settings
from util.debug import set_debuger
if __name__ == "__main__":
    default_settings = Settings()
    args = get_para()
    #print(args)
    startInfo = Handle_para(args, default_settings)
    #print(startInfo)
    debugger = set_debuger(startInfo['mode'])
    debugger.info("啦啦啦啦啦啦")
    debugger.debug("hahahahahaah")
    