from xmlFile import xmlFile
from tag import tag


with open('small.xml', 'r') as file:
    data = file.read().replace('\n', '')
fileToConvert = xmlFile(data)
fileToConvert.getHeaderAndBody()
result = "{\n"
tag = tag(0,"","",[],"",0)
body = tag.getTags(fileToConvert.body, 1)
result += body.formatNameAndAttributes()
result += '}'
print(result)