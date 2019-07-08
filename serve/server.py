import socketserver
from serve.message import Message
from serve.response import Response
import time

def debug(address, DNSrequest, response, mode):
    Time = str(int(time.time()))
    if mode == 1:
        print("+--------------------------------------+")
        print("Time\t:\t" + Time)
        print("ID\t:\t" + str(DNSrequest.header.ID))
        print("From\t:\t" + address[0],":",address[1])
        for i in range(DNSrequest.header.QDCOUNT):
            print("Domain\t:\t" + DNSrequest.questions[i].webname)
        print("+--------------------------------------+\n\n")
    elif mode == 2:
        print("+--------------------------------------+")
        print("Time\t:\t" + Time)
        print("ID\t:\t" + str(DNSrequest.header.ID))
        print("From\t:\t" + address[0],":",address[1])
        print("Flags\t:\t" + '%04X' %DNSrequest.header.FLAGS)
        print("QDCOUNT\t:\t" + str(DNSrequest.header.QDCOUNT))
        print("ANCOUNT\t:\t" + str(DNSrequest.header.ANCOUNT))
        print("NSCOUNT\t:\t" + str(DNSrequest.header.NSCOUNT))
        print("ARCOUNT\t:\t" + str(DNSrequest.header.ARCOUNT))
        for i in range(DNSrequest.header.QDCOUNT):
            print("Domain\t:\t" + DNSrequest.questions[i].webname)
        print("----------------------------------------")
        print("Answers_acount\t:",response.header.ANCOUNT)
        for i in range(response.header.ANCOUNT):
            print("Answers\t\t:" + response.answers[i].get_ip())
        print("+--------------------------------------+\n\n")
    else:
        return

class DNS_handler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        DNSrequest = Message(data)
        #一条正向查询请求
        if DNSrequest.header.QR == 0 and DNSrequest.header.Opcode == 0:
            #处理questions
            #检查请求的域名合法性
            Rtype = self._chech_request(DNSrequest, DNSServer.hosts)
            # 构造返回包
            response = Response(Rtype, DNSrequest, DNSServer.hosts, DNSServer.addr)
            # 发送返回信息
            sock.sendto(response.get_response(), self.client_address)
            # 输出调试信息
            debug(self.client_address, DNSrequest, response, DNSServer.debugMode)

        #非查询请求，返回错误信息
        else:
            Rtype = 0
            # 构造返回包
            response = Response(Rtype, DNSrequest, DNSServer.hosts, DNSServer.addr)
            #发送返回信息
            sock.sendto(response.get_response(), self.client_address)

    @staticmethod
    def _chech_request(request, host):
        _type = 1
        for i in range(request.header.QDCOUNT):
            if request.questions[i].QTYPE != 1:
                _type = 0
                break
            requestDomain = request.questions[i].webname
            if requestDomain in host:
                if host[requestDomain] == '0.0.0.0':
                    _type = 0
        return _type
class DNSServer:
    def __init__(self, settings, startInfo):
        DNSServer.hosts = startInfo['hosts']
        DNSServer.addr = startInfo['addr']
        DNSServer.port = settings.port
        DNSServer.debugMode = startInfo['mode']
        print('Port\t\t\t\t\t:', DNSServer.port)

    def start(self):
        addr = ("127.0.0.1", self.port)
        server = socketserver.ThreadingUDPServer(addr, DNS_handler)
        server.serve_forever()





