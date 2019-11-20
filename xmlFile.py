"""
Small class to convert a string into an xmlFile which allows to ignore the header and return an error if the header is not conform
to xml standards.
"""
class xmlFile():
    def __init__(self, file):
        self.originalFile = file
        self.body = 0

    def getHeaderAndBody(self):
        fileLen = len(self.originalFile)
        if fileLen < 6:
            return (-1)
        if self.originalFile[0:6] != "<?xml ":
            return (-1)
        i = 6
        j = i
        while j < fileLen:
            if self.originalFile[j- 1] == '?' and self.originalFile[j] == '>':
                break
            j += 1
        self.header = self.originalFile[i:j - 1]
        self.body = self.originalFile[j + 1:]
        if self.body[0] != '<':
            return (-1)
        return (0)