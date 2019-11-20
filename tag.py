from usefulFunctions import *

class tag():
    def getTags(self, body, level):
        if body == "":
            return(-1)
        if body[0] != '<':
            return(-1)

        tagName = getName(body)
        i = len(tagName) + 1
        while i < len(body) and body[i] == ' ':
            i += 1

        j = i
        while j < len(body) - i and body[j] != '>':
            j += 1
        if body[j] != '>':
            return(-1) 
        tagAttributes = getAttributes(body, i, j)
        j += 1
        endingIndex = body.find('</' + tagName + '>')
        if endingIndex == -1:
            return (-1)
        tagText = getText(body[j:])
        tagBody = body[j + len(tagText):endingIndex]
        tagLength = j + len(tagText) + len(tagBody) + len(tagName) + 3
        foundTag = tag(tagLength, tagText, tagName, tagAttributes, tagBody, level)
        return(foundTag)
        
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
            newTag = self.getTags(self.inside[i:],level + 1)
            self.tags.append(newTag)
            if newTag == -1:
                break
            i += newTag.length

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
