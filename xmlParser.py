from xmlFile import xmlFile
from tag import tag

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

def nulltag(tagName, level):
    tagText = ""
    tagBody = ""
    tagLength = len(tagName) + 3
    tagAttributes = []
    foundTag = tag(tagLength, tagText, tagName, tagAttributes, tagBody, level)
    return(foundTag)

def getTags(body, level):
    if body == "":
        return(-1)
    #First, we check that the first character is '>'
    if body[0] != '<':
        return(-1)

    #We get tag name with getName func and advance in string to ignore whitespaces
    tagName = getName(body)
    i = len(tagName) + 1
    while i < len(body) and body[i] == ' ':
        i += 1

    #We find the ending '>' to use getAttributes func
    j = i
    while j < len(body) - i and body[j] != '>':
        j += 1
    if body[j] != '>':
        return(-1) 
    tagAttributes = getAttributes(body, i, j)
    j += 1
    #We find ending tag to know if there is a problem and, if not, to get the body of the tag
    endingIndex = body.find('</' + tagName + '>')
    if endingIndex == -1:
        endingIndex = body.find(tagName + '/>')
        if endingIndex == -1:
            return(-1)
        else:
            return(nulltag(tagName, level))
    tagText = getText(body[j:])
    tagBody = body[j + len(tagText):endingIndex]
    tagLength = j + len(tagText) + len(tagBody) + len(tagName) + 3
    foundTag = tag(tagLength, tagText, tagName, tagAttributes, tagBody, level)
    return(foundTag)
        
    
    
def containsTag(body):
    bodyLen = len(body)
    i = 0
    while i < bodyLen:
        if body[i] == '<':
            return(1)
        i += 1
    return (0)

def tabContainsTag(tags):
    tagsLen = len(tags)
    i = 0
    while i < tagsLen:
        if (containsTag(tags[i].inside)):
            return (1)
        i += 1
    return (0)

with open('small.xml', 'r') as file:
    data = file.read().replace('\n', '')
fileToConvert = xmlFile(data)
fileToConvert.getHeaderAndBody()
# print(fileToConvert.header, end="\n\n")
# print(fileToConvert.body, end="\n\n")
result = "{\n"
body = getTags(fileToConvert.body, 1)

i = 0
result += body.formatNameAndAttributes()
result += '}'

print(result)



            






# for elem in tags:
#     result += elem.formatNameAndAttributes()

# i = 0
# j = 0
# tags2 = []
# while j < len(tags1):
#     while len(tags1[0].inside) - i > 0:
#         newTag = getTags(tags1[0].inside[i:], 2)
#         tags2.append(newTag)
#         i += newTag.length
#     j += 1
# k = 0
# for elem in tags2:
#     result += elem.formatNameAndAttributes()
#     if containsTag(elem.inside) == 0:
#         if len(elem.attributes) != 0:
#             result += ((elem.level + 1) * '\t') + '"#text": "' + elem.text + '"\n'
#         else:
#             result = result[:-1]
#             result += '"' + elem.text + '"\n'
#         result += (elem.level * '\t') + '},\n'

        


# i = 0
# j = 0
# tags3 = []
# while j < len(tags2):
#     while len(tags2[0].inside) - i > 0:
#         newTag = getTags(tags2[0].inside[i:], 3)
#         if (newTag != -1):
#             tags2.append(newTag)
#             i += newTag.length
#         else:
#             break
#     j += 1

# print(result)
