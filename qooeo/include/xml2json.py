import xmltodict;
import json;
 
def pythonXmlToJson():
    """
        demo Python xml to json
    """
    xmlStr = """
<student>
    <stid>10213</stid>
    <info>
        <name>name</name>
        <mail>xxx@xxx.com</mail>
        <sex>male</sex>
    </info>
    <course>
        <name>math</name>
        <score>90</score>
    </course>
    <course>
        <name>english</name>
        <score>88</score>
    </course>
</student>
"""
 
    convertedDict = xmltodict.parse(xmlStr);
    print (convertedDict)
    jsonStr = json.dumps(convertedDict);
    print ("jsonStr=",jsonStr)
    xml_str = xmltodict.unparse(convertedDict)
    print (xml_str)
pythonXmlToJson()