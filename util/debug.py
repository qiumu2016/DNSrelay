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