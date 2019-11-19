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

class tag():
    def __init__(self, length, text, name, attributes, inside, level):
        self.length = length
        self.text = text
        self.name = name
        self.attributes = attributes
        self.inside = inside
        self.level = level
        self.tags = []
        i = 0
        while i < len(self.inside):
            newTag = getTags(self.inside[i:],level + 1)
            self.tags.append(newTag)
            if newTag == -1:
                break
            i += newTag.length

    def __str__(self):
        toPrint = "length = " + str(self.length) + "\n\n"
        toPrint = "level = " + str(self.level) + "\n\n"
        if len(self.text) > 0:
            toPrint += "text = "
            toPrint += self.text + "\n\n"
        else:
            toPrint += "No text.\n\n"
        toPrint += "name = "
        toPrint += self.name + "\n\n"
        if len(self.attributes) > 0:
            toPrint += "Attributes:" + '\n'
            i = 1
            for elem in self.attributes:
                toPrint += "name: " + elem[0] + " "
                toPrint += "value: " +elem[1] + "\n"
                i += 1
        else:
            toPrint += "No attributes."
        toPrint += "\n\n"
        toPrint += "Body:" + '\n'
        toPrint += self.inside + '\n\n'
        if len(self.tags) > 0:
            toPrint += "Embedded tags:" + '\n'
            for elem in self.tags:
                print(elem)
                toPrint += elem.name + '\n'
        else:
            toPrint += "No embedded tags\n"
        toPrint += '\n' + '--------------------------------------' + '\n'
        return(toPrint)

    def formatText(self):
        if len(self.attributes) == 0:
            return ('"' + self.text + '",\n')
        elif len(self.tags) == 0:
            return(((self.level + 1) * '\t') + '"#text": ' + self.text + '",\n' + self.level * '\t' + '},\n')
        else:
            return(((self.level + 1) * '\t') + '"#text": ' + self.text + '",\n')



    def formatNameAndAttributes(self):
        jsonFormat = (self.level * '\t') + '"' + self.name + '": '
        if len(self.attributes) > 0 or len(self.tags) > 0:
            jsonFormat += '{\n'
            for elem in self.attributes:
                jsonFormat += self.level * '\t' +'\t"@' + elem[0] +'": ' + elem[1] + ',\n'
        if len(self.tags) == 0:
            jsonFormat += self.formatText()
        else:
            for elem in self.tags:
                if elem != -1:
                    jsonFormat += elem.formatNameAndAttributes()
            if self.text != "":
                jsonFormat += self.formatText()
            jsonFormat += self.level * '\t' + '},\n'
        return(jsonFormat)
