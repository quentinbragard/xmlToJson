def getName(body):
    i = 1
    fileLen = len(body)
    while i < fileLen and body[i] != ' ' and body[i] != '>':
        i += 1
    if body[i] != ' ' and body[i] != '>':
        return (-1)
    tagName = body[1:i]
    return (tagName)

def getAttributes(body, i, j):
    if i == j:
        return([])
    tagAttributes = body[i:j].split(' ')
    k = 0
    while k < len(tagAttributes):
        values = tagAttributes[k].split('=')
        if len(values) > 2:
            real_value = '='.join(values[1:])
            values[1] = real_value
        tagAttributes[k] = values
        k += 1
    return(tagAttributes)

def getText(body):
    i = 0
    fileLen = len(body)
    while i < fileLen and body[i] != '<':
        i += 1
    text = body[:i]
    return (text)


