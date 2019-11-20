from xmlFile import xmlFile
from tag import tag

"""
The only work performed by the parser is to create a string, which would be json formated thanks to the tag class and 
the two jsonFormat functions. There is a unique call to the formatNameAndAttributes method which is recursive and a
unique call to the getTags method which is also recursive. We need to create an empty tag "tag" to call the getTags method. 

It also use the xmlFile class.
"""

with open('small.xml', 'r') as file:
    data = file.read().replace('\n', '')
fileToConvert = xmlFile(data)
fileToConvert.getHeaderAndBody()
result = "{\n"
tag = tag(0,"","",[],"",0)
body = tag.getTags(fileToConvert.body, 1)
result += body.formatNameAndAttributes()
result += '}'
result = result[:-3] + result[-2:]
#uncomment the following line to print the ouput
#print(result)

with open('small.json', 'w') as outfile:
    outfile.write(result)