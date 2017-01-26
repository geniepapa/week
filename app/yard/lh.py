# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='TNCQD109INT001'):

    session = requests.session()
    session.get("http://221.215.96.158:8086/root/jsp/")
    login_data = {
        'strlogname': 'guest',
        'strpwd': 'guest',
        'submit1': '(unable to decode value)'
    }
    login_response = session.post("http://221.215.96.158:8086/root/jsp/login.jsp", data=login_data)

    session.get("http://221.215.96.158:8086/root/jsp/search/search0402.jsp")

    data = {
        'BillNo': bl_num.strip(),
        'submit1': '(unable to decode value)'
    }

    response = session.post("http://221.215.96.158:8086/root/jsp/search/search0402.jsp", data=data)

    html = etree.HTML(response.text)

    # html = etree.HTML(response.text)

    info_html = html.xpath("//body/div")

    if len(info_html) > 0:

        elem_div = info_html[0].xpath("div")[0]
        elem_div.getparent().remove(elem_div)

        elem_brs = info_html[0].xpath("br")
        for elem_br in elem_brs:
            elem_br.getparent().remove(elem_br)


        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
