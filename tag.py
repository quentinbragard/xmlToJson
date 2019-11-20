from usefulFunctions import *
"""
    The tag class contains different attributes: 
        - Name: teh name of the tag. For example , the tag "<test att1="val1" att2="val2">something is written here</test>",
        would be "test".

        - Length: it is the length of the defining string. In the previous example, le length would be 62 (the '>' and '<' are counted).
        
        -Text: it is the texte contained between two tags. It won't ever contain an embedded tag. In our example, it would be
        "something is written here".

        -Attributes: it is a list containing all specified attributes in the openoing tag. Here it would be: [[att1,val1], [att2,val2]].

        -Inside: it is the raw string that is used to get all tags. in our example, the inside would be: 
        "<test att1="val1" att2="val2">something is written here</test>".

        -Tags: it is a list of all embeded tags contained in our tag. Each time a tag is created, the recursive function getTags is called to fill
        this list which will create the embedded tags by calling herself until there are no more embedded tags (return -1). In our example, 
        there are no embedded tags, so the retyurn would directly be -1. 

        -Level: it refers to the question of embedded tags. the first level is level 1 and concerns the body tag of the xml. Then each tag
        contained into it would be a level 2 tag and each tag contained in this contained tag would be a level 3 tag, etc. It will be used
        in order to get the indenttion level when formating the json string.

    Among the getTags and the __init__ and __str__ functions, there are two functions that would be used in order to convert the tag class into a json
    formated string. The main one in Format NameandAttributes which is a recursive function formatting the name as well as the attributes and calls
    formatText if there are no embeded tags or calls itself of there are embedded tags to format the enbedded tags. 
"""

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
