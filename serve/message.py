import struct
class Message:
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
    def __init__(self, data):
        self.header = Header(data[0:12])
        self.questions = []
        self.answers = []
        self.authorities = []
        self.additionals = []
        index = 12
        if self.header.QDCOUNT != 0 :
            index = self._handle_question(data, index)
        if self.header.ANCOUNT != 0 :
            index = self._handle_resource(data, index, self.answers, self.header.ANCOUNT)
        if self.header.NSCOUNT != 0 :
            index = self._handle_resource(data, index, self.authorities, self.header.NSCOUNT)
        if self.header.ARCOUNT != 0 :
            index = self._handle_resource(data, index, self.additionals, self.header.ARCOUNT)



    def _handle_question(self, data, index):
        for i in range(self.header.QDCOUNT):
            next_index = index + data[index:].find(0) + 5
            self.questions.append(Question(data[index:next_index]))
            index = next_index
        return index
    def _handle_resource(self, data, index, rlist, count):
        next_index = index
        for i in range(count):
            if data[next_index] >> 6 == 3:
                start = next_index + 2
            else:
                start = next_index + data[next_index:].find(0) + 1
            Rtype, Rclass, Rttl, Rdlengh = struct.unpack('>HHIH',data[start:start+10])
            rlist.append(Resource(data[next_index:start], Rtype, Rclass, Rttl, Rdlengh, data[start+10:start+10+Rdlengh]))
            next_index = start + 10 + Rdlengh
        return next_index

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
    def __init__(self,data):
        self.ID, self.FLAGS, self.QDCOUNT, self.ANCOUNT, self.NSCOUNT, self.ARCOUNT = struct.unpack('>HHHHHH',data)
        self.QR = bytes([(self.FLAGS >>15)])
        self.Opcode = bytes([(self.FLAGS << 1 >> 12)])
        self.AA = bytes([(self.FLAGS << 5 >> 15)])
        self.TC = bytes([(self.FLAGS << 6 >> 15)])
        self.RD = bytes([(self.FLAGS << 7 >> 15)])
        self.RA = bytes([(self.FLAGS >> 7 & 0x01)])
        self.Z = bytes([(self.FLAGS >> 4 & 0x07)])
        self.RCODE = bytes([(self.FLAGS & 0x0f)])
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
    def __init__(self, data):
        self.QTYPE, self.QCLASS = struct.unpack('>HH',data[-4:])
        self.QNAME = data[:-4]
        if self.QTYPE == 1 :
            self.webname = self._get_webname(self.QNAME)
        elif self.QTYPE == 2:
            self.ip = self.QNAME

    def _get_webname(self,data):
        i = 1
        webname = ''
        while True:
            char = data[i]
            if char == 0:
                break
            if char < 32:
                webname = webname + '.'
            else:
                webname = webname + chr(char)
            i = i + 1

        return webname


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
    def __init__(self, rname, rtype, rclass,rttl, rdlength, rdata ):
        self.NAME = rname
        self.TYPE = rtype
        self.CLASS = rclass
        self.TTL = rttl
        self.RDLENGTH = rdlength
        self.RDATA = rdata



