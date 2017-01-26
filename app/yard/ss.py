# coding: utf-8
import requests
from lxml import etree


def grab(bl_num='ESLQA11415'):

    session = requests.session()
    data = {
        '__LASTFOCUS': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwUKLTU5ODYxMzQ0MQ9kFgICAw9kFgoCCw8PZBYCHgVzdHlsZQUMZGlzcGxheTpub25lZAIVDzwrABEBARAWABYAFgBkAhcPD2QWAh8ABQxkaXNwbGF5Om5vbmVkAhkPPCsAEQBkAh0PZBYEAgEPD2QWAh8ABQxkaXNwbGF5Om5vbmVkAgMPD2QWAh8ABQxkaXNwbGF5Om5vbmVkGAIFCUdyaWRWaWV3Mg9nZAUJR3JpZFZpZXcxD2dkBGQZMyDKgDrmB/pQtd0PWhr+MXX7N7CaIqVBhit/jps=',
        '__VIEWSTATEGENERATOR': '4FCC0923',
        'TextBox1': bl_num.strip(),
        'Button1': u'查询'

    }
    response = session.post("http://www.ssqd.cn/Scfs.aspx", data=data)

    html = etree.HTML(response.text.encode(response.encoding))

    info_tables = html.xpath("//form/table[3]|//form/table[4]")

    info = ""
    if info_tables:
        for info_table in info_tables:

            elem_links = info_table.xpath("//a")
            for elem_link in elem_links:
                elem_link.set("href", "#")

            info = info + etree.tostring(info_table, pretty_print=True) + "</br>"

    session.close()

    return info


if __name__ == '__main__':
    grab()
