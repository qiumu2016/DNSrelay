import socketserver
from util.debug import set_debuger
from serve.message import Message
from serve.message import Header
from serve.message import Question
from serve.message import Resource

class DNS_handler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        DNSrequest = Message(data)
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





