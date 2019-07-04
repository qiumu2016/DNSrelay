import socketserver
from util.debug import set_debuger
from serve.message import Message
from serve.response import Response

class DNS_handler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        DNSrequest = Message(data)
        hostRecord = DNSServer.hosts
        #一条正向查询请求
        if DNSrequest.header.QR == 0 and DNSrequest.header.Opcode == 0:
            #处理questions
            #检查请求的域名合法性
            Rtype = self._chech_request(DNSrequest, hostRecord)
            #构造返回包
            # TO DO
            response = Response(Rtype, DNSrequest).get_response()
            # 发送返回信息
            sock.sendto(response, self.client_address)
        #一条反向查询请求
        elif DNSrequest.header.QR == 0 and DNSrequest.header.Opcode == 1:
            Rtype = 2
            # 构造返回包
            # TO DO
            response = Response(Rtype, DNSrequest).get_response()
            # 发送返回信息
            sock.sendto(response, self.client_address)
        #非查询请求，返回错误信息
        else:
            Rtype = 0
            # 构造返回包
            # TO DO
            response = Response(Rtype, DNSrequest).get_response()
            #发送返回信息
            sock.sendto(response, self.client_address)

    @staticmethod
    def _chech_request(self, request, host):
        _type = 1
        for i in range(request.header.QDCOUNT):
            requestDomain = request.questions[i].webname
            if requestDomain in host:
                if host[requestDomain] == '0.0.0.0':
                    _type = 0
                    return _type
        return _type

        #print('DNSrequest:', DNSrequest.header)
        #print('details:', DNSrequest.questions[0])
        #print('items:', ', '.join(['%s:%s' % item for item in DNSrequest.header.__dict__.items()]))
        #print('FLAGS:',bytes([DNSrequest.header.FLAGS >> 8]))
        #print('items:', ', '.join(['%s:%s' % item for item in DNSrequest.questions[0].__dict__.items()]))
        #dnsRequest =
        #DNSServer.debugger.debug("working ...")

class DNSServer:
    def __init__(self, settings, startInfo):
        DNSServer.hosts = startInfo['hosts']
        DNSServer.addr = startInfo['addr']
        DNSServer.port = settings.port
        DNSServer.debugger = set_debuger(startInfo['mode'])
        DNSServer.debugger.info('Remote DNS server addrss = %s, port = %s ',DNSServer.addr, DNSServer.port)

    def start(self):
        addr = ("127.0.0.1", self.port)
        server = socketserver.ThreadingUDPServer(addr, DNS_handler)
        server.serve_forever()





