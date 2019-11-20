import xmltodict
import json

with open('small.xml') as fd:
    doc = xmltodict.parse(fd.read(), process_namespaces=False)
with open('test.json', 'w') as outfile:
    json.dump(doc, outfile, indent=6)