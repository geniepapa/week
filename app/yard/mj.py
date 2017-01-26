
import requests
from lxml import etree


def grab(bl_num='APLU666214128'):

    session = requests.session()
    data = {
        'bill_no': bl_num.strip(),
        'summit': '(unable to decode value)'

    }
    response = session.get("http://www.gfqd.com.cn/bill_no_query.asp", data=data)

    html = etree.HTML(response.text.encode(response.encoding))


    info_html = html.xpath("//body")

    if len(info_html) > 0:

        elem_links = info_html[0].xpath("//a")
        for elem_link in elem_links:
            elem_link.getparent().remove(elem_link)

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
