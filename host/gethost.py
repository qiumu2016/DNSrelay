def gethost(fileName):
    f = open(fileName, 'r')
    data = f.read()
    f.close()
    contents = data.split('\n')
    result = {}
    for content in contents:
        record = content.split(' ')
        ip = record[0]
        domain = record[1]
        result.update({domain: ip})
    return result