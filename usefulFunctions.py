"""
Those functions are designed to be used in the getTags method of thge tag class. They will respectively read the name, the attributes 
and the text contained in each tag. Those functions are each time a new tag is detected. So far it does not handle the <tag/> case, neitehr
the multiple text case. 
"""


def getName(body):
    i = 1
    fileLen = len(body)
    while i < fileLen and body[i] != ' ' and body[i] != '>':
        i += 1
    if body[i] != ' ' and body[i] != '>':
        return (-1)
    #Here, we could change the implementation to accept the <unique/> tags by checking if we have a body[i-1] == '/'
    #and body[i] =='>'. In that case, we would have tagName = body[1:i - 1]. Be careful to tag.length then... 
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
    #in the case of a <unique/> tag, we would return ("") anyway. 
    return (text)


