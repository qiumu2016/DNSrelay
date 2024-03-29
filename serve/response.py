"""
    根据收到的请求组包，分为两个类型：
        type == 0 ：正向查询，查询ip为0.0.0.0，返回错误信息
        type == 1 ：正向查询，合法ip,包括本地和远程
"""
import dns.resolver
import struct

class Response:
    """
    ┏━━━━━━━━━━
    ┃      Header       ┃  6部分，共12字节
    ┃━━━━━━━━━ ┃
    ┃     Question      ┃  查询区域
    ┃━━━━━━━━━ ┃
    ┃     Answer        ┃  回答区域
    ┃━━━━━━━━━ ┃
    ┃     Authority     ┃  授权区域
    ┃━━━━━━━━━ ┃
    ┃     Additional    ┃  附加区域
    ┃━━━━━━━━━ ┃
    """
    #TO DO
    def __init__(self, rtype, request, hostRecord, remoteAddr):
        self.host = hostRecord
        self.rtype = rtype
        self.questions = []
        self.answers = []
        self.authorities = []
        self.additionals = []
        self.remoteAdrr = remoteAddr
        # 正向查询，为0.0.0.0
        if rtype == 0:
            _id = request.header.ID
            _flags = 32773
            self.header = Header(_id, _flags, 0, 0, 0, 0)
            for i in range(request.header.QDCOUNT):
                self.questions.append(Question(request.questions[i].QNAME, request.questions[i].QCLASS, request.questions[i].QTYPE))
        #正向查询
        else:
            _id = request.header.ID
            _flags = 33152
            self.header = Header(_id, _flags, request.header.QDCOUNT, request.header.QDCOUNT, 0, 0)
            for i in range(request.header.QDCOUNT):
                self.questions.append(
                    Question(request.questions[i].QNAME, request.questions[i].QCLASS, request.questions[i].QTYPE))
                _ip = self._get_ip(request.questions[i])
                if _ip is not None:
                    self.answers.append(Resource(request.questions[i].QNAME, 1, 1, 86400, 4, _ip))
                    hostRecord.update({request.questions[i].webname: _ip})
                else:
                    self.answers.append(Resource(request.questions[i].QNAME, 1, 1, 86400, 4, '0.0.0.0'))
    # 查询ip
    def _get_ip(self, question):
        requestDomain = question.webname
        # 本地存在
        if requestDomain in self.host:
            _ip = self.host[requestDomain]
        # 本地不存在
        else:
            remoteList = [self.remoteAdrr]
            my_resolver = dns.resolver.Resolver()
            my_resolver.nameservers = remoteList
            try:
                res = my_resolver.query(requestDomain, 'A')
                _ip =  str(res[0])
            except Exception:
                _ip =  None
        return _ip
    # 序列化输出
    def get_response(self):
        res = self.header.get_header()
        #非法请求，只有头部
        if self.rtype == 0:
            return res
        else:
            for i in range(self.header.QDCOUNT):
                res += self.questions[i].get_question()
        if self.answers is not None:
            for i in range(len(self.answers)):
                res += self.answers[i].get_resource()

        return res

class Header:
    """
     0  1  2  3  4  5  9  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       | 消息ID，请求和应答相同，2字节
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|    Z   |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |   问题数，2字节，无符号16位整数
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |   回答资源记录数，2字节，无符号16位整数
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |   授权资源记录数，2字节，无符号16位整数
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |   附加资源记录数，2字节，无符号16位整数
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

    QR（1bit）	查询/响应标志，0为查询，1为响应
    opcode（4bit）	0表示标准查询，1表示反向查询，2表示服务器状态请求
    AA（1bit）	表示授权回答
    TC（1bit）	表示可截断的 ，0 为报文未截断 ，1 为报文过长被截断 (只返回了前 512 个字节)
    RD（1bit）	表示期望递归 ，0 为不期望进行递归查询 ，1 为期望进行递归查询 (从域名服务器进行递归查询)
    RA（1bit）	表示可用递归 ，0 为应答服务器不支持递归查询 ，1 为应答服务器支持递归查询
    Z（3bit）   未使用，必须置0
    rcode（4bit）	表示返回码，0表示没有差错，3表示名字差错，2表示服务器错误（Server Failure）
    """
    def __init__(self, _id, flags, qdcount, ancount, nscount, arount):
        self.ID = _id
        self.FLAGS = flags
        self.QDCOUNT = qdcount
        self.ANCOUNT = ancount
        self.NSCOUNT = nscount
        self.ARCOUNT = arount
    def get_header(self):
        res = struct.pack('>HHHHHH', self.ID, self.FLAGS, self.QDCOUNT, self.ANCOUNT, self.NSCOUNT, self.ARCOUNT)
        return res

class Question:
    """
    0  1  2  3  4  5  9  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |  查询名字，长度不固定，不使用填充字节，如果是反向查询，则为IP，
    /                     QNAME                     /  每个标识符以首字节的计数值来说明随后标识符的字节长度，
    /                                               /  每个名字以最后字节为0结束
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |   2字节，查询类型，取值可以为任何可用的类型值
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |   2字节，查询类：通常为1，表示IN，表明是Internet数据。
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """
    def __init__(self, _name, _type, _class):
        self.QTYPE = struct.pack('>H',_type)
        self.QCLASS = struct.pack('>H',_class)
        self.QNAME = _name

    def get_question(self):
        return self.QNAME + self.QTYPE + self.QCLASS


class Resource:
    """
    资源记录（包括回答区域，授权区域和附加区域）
     0  1  2  3  4  5  9  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |  它的格式和Queries区域的查询名字字段是一样的
    /                      NAME                     /  当报文中域名重复出现的时候，该字段使用2个字节的偏移指针来表示
    /                                               /  前两位 11，用于识别指针。后14位从DNS报文的开始处计数（从0开始），指出该报文中的相应字节数
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |   2字节，查询类型，取值可以为任何可用的类型值，与question相同
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      CLASS                    |   2字节，查询类：通常为1，表示IN，表明是Internet数据。
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                 Time To Live(TTL)             |   4字节无符号整数表示资源记录可以缓存的时间。 以秒为单位，
    |                                               |  表示的是资源记录的生命周期，用于当地址解析程序取出资源记录后决定保存及使用缓存数据的时间
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     RDLENGTH                  |   2字节，无符号整数表示RDATA的长度
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
     |                      RDATA                   |   可变长字段，不定长字符串来表示记录，格式与TYPE和CLASS有关
     /                                              /
     /                                              /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """
    def __init__(self, rname, rtype, rclass, rttl, rdlength, rdata):
        self.NAME = rname
        self.TYPE = struct.pack('>H',rtype)
        self.CLASS = struct.pack('>H',rclass)
        self.TTL = struct.pack('>L',rttl)
        self.RDLENGTH = struct.pack('>H',rdlength)
        self.RDATA = rdata

    def get_resource(self):
        res = self.NAME + self.TYPE + self.CLASS + self.TTL + self.RDLENGTH
        ip = self.RDATA.split('.')
        res += struct.pack('BBBB', int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3]))
        return res
    def get_ip(self):
        return self.RDATA



