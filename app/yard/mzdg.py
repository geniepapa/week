# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='OOLU2583212290'):

    session = requests.session()

    data = {
        'tdh': bl_num.strip(),
        'btnQueryBill': '(unable to decode value)'
    }
    response = session.post("http://www.qingdaoportec.net/nqoct/qoctdList.action", data=data)

    html = etree.HTML(response.text)

    info_html = html.xpath("//body/table[4]/tr/td/table[2]")

    if len(info_html) > 0:

        elem_links = info_html[0].xpath("//a")
        for elem_link in elem_links:
            elem_link.set("href", "#")

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
