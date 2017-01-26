# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='HDMUQIAE4311854'):

    session = requests.session()

    data = {
        'BL_NO': bl_num.strip(),
        'x': '45',
        'y': '7'
    }

    session.post("http://www.sjhlco.com/InfoService/blinfo", data=data)
    session.get("http://www.sjhlco.com/InfoService/")
    session.get("http://www.sjhlco.com/InfoService/blinfo")

    response = session.post("http://www.sjhlco.com/InfoService/blinfo", data=data)

    html = etree.HTML(response.text)

    info_divs = html.xpath("//div[@class='clfix box_tbl_ty3 mgt8']")

    info = ""
    if info_divs:
        for info_div in info_divs:

            elem_links = info_div.xpath("//a")
            for elem_link in elem_links:
                elem_link.set("href", "#")

            info = info+etree.tostring(info_div, pretty_print=True)+"</br>"

    session.close()

    return info


if __name__ == '__main__':
    grab()
