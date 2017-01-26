
import requests
from app.util.ocr import ocr_response
from lxml import etree
import simplejson as json

def grab(page, bl_num):
    session = requests.session()

    session.get("http://www.qingdaoport.net/ywzx/qqct/dpcx/"+page)
    captcha_response = session.get("http://www.qingdaoport.net/adv/random.jsp")
    captcha = ocr_response(captcha_response)

    print(captcha)

    response = session.post("http://www.qingdaoport.net/ywzx/qqct/dpcx/crpcx.jsp", data={
        'tdh': bl_num,
        'num': captcha})

    # html = etree.HTML(unicode.encode(response.text, encoding='utf-8'))

    html = etree.HTML(response.text)
    info_html = html.xpath("body/table[3]/tr/td/table/tr[4]/td")
    if len(info_html) > 0:
        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info
