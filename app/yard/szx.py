# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='PASU5047650340'):

    session = requests.session()
    data = {
        '__VIEWSTATE':'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',
        'ctl00$Maincontent$txtBillNo': bl_num.strip(),
        'ctl00$Maincontent$btnSearch': u'查询'
    }
    response = session.post("http://www.szx.net.cn/querydata/billquerysearch.aspx", data=data)

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
