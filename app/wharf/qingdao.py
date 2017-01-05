# coding: utf-8

import requests
from app.util.ocr import orc_response
from lxml import etree


def grab(vessel='JI HAI ZHI XING', voyage='16094S'):

    session = requests.session()
    session.get("http://www.qingdaoport.net/ywzx/ship/shipcx.jsp")

    captcha_response = session.get("http://www.qingdaoport.net/adv/random.jsp")
    captcha = orc_response(captcha_response)

    print(captcha)

    response = session.post("http://www.qingdaoport.net/ywzx/ship/shipcx.jsp", data={
        'vessel_name': vessel,
        'voyage_number': voyage,
        'num': captcha})

    # html = etree.HTML(unicode.encode(response.text, encoding='utf-8'))
    html = etree.HTML(response.text)
    session.close()

    info = []

    columns = html.xpath('//table')[7][2].getchildren()

    if columns and len(columns) > 2:
        info.append({
            'status': columns[8].text,
            'wharf': columns[0].find('b').text,
            'local': columns[15].text,
            'ship': columns[6].text,
            'eta': columns[9].text,
            'ata': columns[10].text,
            'etd': columns[11].text,
            'atd': columns[12].text,
            'piling': columns[13].text,
            'unpiling': columns[14].text
        })

    return info
