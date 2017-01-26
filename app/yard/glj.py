# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='TNCQD205IMM502'):

    session = requests.session()
    data = {
        '__VIEWSTATE':'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',
        'ctl00$Maincontent$txtBillNo': bl_num.strip(),
        'ctl00$Maincontent$btnSearch': u'查询'
    }
    session.get("http://www.worldex.com.cn/glj/querydata/billquerysearch.aspx")
    response = session.post("http://www.worldex.com.cn/glj/querydata/billquerysearch.aspx",data=data)

    html = etree.HTML(response.text.encode(response.encoding))

    # html = etree.HTML(response.text)

    info_html = html.xpath("//div[@id='Maincontent_divform']")

    if len(info_html) > 0:

        elem_links = info_html[0].xpath("//a")
        for elem_link in elem_links:
            elem_link.set("href", "#")

        elem_tables = info_html[0].xpath("//table")
        for elem_table in elem_tables:
            elem_table.set("style", "")

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
