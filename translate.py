from pygtrans import Translate
from cfg import LANGUAGES
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.dom import minidom
import os

if __name__ == "__main__":
    desXmlFilePath = input("请输入目标路径：")
    srcXmlFilePath = desXmlFilePath+"/values/strings.xml"
    client = Translate()
    # client.detect('谷歌翻译').language
    # 'zh-CN'
    # # 单个
    # text = client.translate('Hello, Google,jack')
    # print(text.translatedText)

    # 获取需要翻译的字符串列表
    tree = ET.parse(srcXmlFilePath)
    root = tree.getroot()
    # 需要翻译的中文文案列表
    srcList = []
    # 翻译后对应语言的文案列表
    desList = []
    # 获取中文文案列表
    for index in range(0, len(root)):
        if root[index].tag == 'string' and 'msgid' not in root[index].attrib.keys():
            srcList.append(root[index].text)

    # 开始翻译并生成对应语言的xml文件
    for language in LANGUAGES.keys():
        # 批量翻译
        desList = client.translate(srcList, target=language)
        # 创建对应语言的xml字符串
        res = Element('resources') 
        for index in range(0, len(root)):
            s = ET.SubElement(res, root[index].tag)
            s.attrib = root[index].attrib
            s.text = desList[index].translatedText

        # 格式化xml字符串
        xmlString = ET.tostring(res)
        newTree = minidom.parseString(xmlString)
        xmlString = newTree.toprettyxml()
        print(xmlString)

        # 矫正文件夹后缀
        if "-" in language:
            s = language.split("-")
            language = s[0]+"-r"+s[1].upper()

        # 将xml写入文件
        path = desXmlFilePath + "/values-" + language
        if not os.path.exists(path):
            os.mkdir(path)
        fileName = path + '/strings.xml'
        xmlFile = open(fileName, 'w', encoding='utf-8')
        newTree.writexml(xmlFile, "", "\t", "\n", encoding='utf-8')
