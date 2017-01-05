import requests
from lxml import etree

content_url = "http://www.cma-cgm.com/ebusiness/tracking/search"


def grab(bl_num='NAM2486916'):

    routes = []
    containers = []

    session = requests.session()
    data = {'SearchBy': 'BL', 'Reference': str.strip(bl_num)}
    # session.get(session_url)
    response = session.get(content_url, params=data)

    print response.text

    if response.status_code == 200:
        cma_doc = etree.HTML(unicode.encode(response.text, encoding='utf-8'))


        containers_doc = cma_doc.xpath("//tr[@class='container-row']")
        routes_doc = cma_doc.xpath("//tr[@class='small-data-info']")

        try:
            for index, container in enumerate(containers_doc):
                container_td = container.getchildren()
                if index == 0:
                    routes.append({
                        'route_name': 'Discharge Port',
                        'location': container_td[3].text.strip(),
                        'vessel': container_td[8].text.strip(),
                        'voyage': container_td[7].text,
                        'call_sign': '',
                        'estimate_arrival_date': '',
                        'actual_arrival_date': '',
                        'container_load_date': '',
                        'container_discharge_date': container_td[2].text.strip(),
                        'estimate_departure_date': '',
                        'actual_departure_date': ''})
                containers.append({
                    'number': container_td[1].getchildren()[0].text.strip(),
                    'status': container_td[4].text.strip(),
                    'type': container_td[6].getchildren()[0].text[2:],
                    'size': container_td[6].getchildren()[0].text[:2],
                    'height': '',
                    'location': container_td[3].text.strip(),
                    'container_load_date': '',
                    'container_discharge_date': container_td[2].text.strip()
                })

        except Exception, e:
            print(Exception, ":", e)

    return {'routing': routes, 'containers': containers}
