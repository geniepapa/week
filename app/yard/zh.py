# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='NYKSTA6OS5467100'):

    session = requests.session()

    data = {
        'tidan': bl_num.strip(),
        'x': '24',
        'y': '5'
    }
    response = session.post("http://www.qdzh-logistics.com/search/searchBillCase!findByBillNo", data=data)

    html = etree.HTML(response.text)

    # html = etree.HTML(response.text)

    info_html = html.xpath("//div[@id='mainContent']/table[2]")

    if len(info_html) > 0:

        elem_links = info_html[0].xpath("//a")
        for elem_link in elem_links:
            elem_link.set("href", "#")

        elem_imgs = info_html[0].xpath("//img")
        for elem_img in elem_imgs:
            elem_img.getparent().remove(elem_img)

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
