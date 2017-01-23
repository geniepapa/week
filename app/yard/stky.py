
import requests
from lxml import etree


def grab(bl_num='TNCQD204IMM505'):

    session = requests.session()
    session.get("http://www.stx-keyun.com/query/index.asp")

    data = {
        'BL_NO1': bl_num.strip(),
        'submit1': '(unable to decode value)'
    }

    response = session.post("http://www.stx-keyun.com/query/search_bl_no.asp", data=data)
    # response_content = unicode.decode(response.text, encoding='utf-8')

    html = etree.HTML(response.text.encode(response.encoding))

    # html = etree.HTML(response.text)

    info_html = html.xpath("//div[@class='content1']")

    if len(info_html) > 0:

        elem_form = info_html[0].find("form")
        elem_a = info_html[0].find("a")

        info_html[0].remove(elem_form)
        info_html[0].remove(elem_a)

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
