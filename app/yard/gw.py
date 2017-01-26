# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='MCT559907'):

    session = requests.session()
    response = session.get("http://www.penavicogw.com/%E6%8F%90%E5%8D%95%E6%9F%A5%E8%AF%A2-2/?billno="+bl_num+"&queryflag=%E6%9F%A5%E8%AF%A2")

    html = etree.HTML(response.text.encode(response.encoding))

    info_html = html.xpath("//div[@class='DRight']/div[2]")

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
