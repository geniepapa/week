
import requests
from lxml import etree


def grab(bl_num='575400013'):

    session = requests.session()
    response = session.get("http://www.sdsmartlogistics.com/Search/YD_BLQueryGrid.aspx?blno="+bl_num)

    html = etree.HTML(response.text)

    # html = etree.HTML(response.text)

    info_html = html.xpath("//div[@id='exptable']")

    if len(info_html) > 0:

        elem_tr = info_html[0].find("table/tr[1]")
        elem_input = info_html[0].find("table/tr[8]/td/input")

        elem_tr.getparent().remove(elem_tr)
        elem_input.getparent().remove(elem_input)

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
