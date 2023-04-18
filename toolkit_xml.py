from lxml import etree

import xmltodict
import json


def xml_minify(xml_str):
    parser = etree.XMLParser(remove_blank_text=True)
    xml_str = bytes(bytearray(xml_str, encoding='utf-8'))
    elem = etree.XML(xml_str, parser=parser)
    return etree.tostring(elem, xml_declaration=True, encoding='utf-8').decode().replace('\n', '')


def xml2dict(xmlString):
    '''Return json object'''
    jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
    xml_in_json = json.loads(jsonString)
    return xml_in_json


if __name__ == '__main__':
    xmlsample = 'api_export/getListformated_sample.xml'

    xmlString = open(xmlsample, encoding = 'utf-8').read()
    xmlsamplejson = xml2dict(xmlString)
    update_date = xmlsamplejson['feed']['modified']

    # with open('api_export/test.json', 'w') as f:
    #     f.write(jsonString)
