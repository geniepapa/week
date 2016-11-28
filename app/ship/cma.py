import requests
from lxml import etree

#session_url = "http://homeport.apl.com/gentrack/trackingMain.do"
content_url = "http://www.cma-cgm.com/ebusiness/tracking/search"


def grab(bl_num='NAM2486916'):
    session = requests.session()
    data = {'SearchBy': 'BL', 'Reference': str.strip(bl_num)}
    # session.get(session_url)
    response = session.get(content_url, params=data)

    cma_doc = etree.HTML(unicode.encode(response.text, encoding='utf-8'))

    containers_doc = cma_doc.xpath("//tr[@class='container-row']")

    containers = []
    for container in containers_doc:
        container_td = container.getchildren()
        containers.append({
            'number': container_td[0].text.strip(),
            'status': '',
            'type': container_td[1],
            'size': container_td[2],
            'height': '',
            'location': '',
            'container_load_date': '',
            'container_discharge_date': ''
        })




    return response.text
