import requests
from lxml import etree

content_url = "http://www.shipmentlink.com/servlet/TDB1_CargoTracking.do"


def grab(bl_num='003602132872'):
    session = requests.session()
    data = {
        'BL':  str.strip(bl_num),
        'TYPE': 'BL',
        'SEL': 's_bl',
        'NO': str.strip(bl_num)
    }
    session.get(content_url)
    response = session.post(content_url, params=data)
    return html_parse(response)


routes_xpath = "//body/table[3]/tr/td/table[1]/tr"
routes_extend_xpath = "///body/table[3]/tr/td/table[2]/tr"
container_xpath = "//body/table[3]/tr/td/table[3]/tr"


def html_parse(response):

    routes_doc, containers_doc = get_docs(response.text)
    return {'routing': get_routes(routes_doc), 'containers': get_containers(containers_doc)}


def get_docs(content):

    doc = etree.HTML(unicode.encode(content, encoding='utf-8'))
    containers_doc = doc.xpath(container_xpath)
    routes_doc = doc.xpath(routes_xpath)

    routes_extend_doc = doc.xpath(routes_extend_xpath)
    routes_doc[0].extend([
        routes_extend_doc[2].find("td[2]"),
        routes_extend_doc[3].find("td[2]"),
        routes_extend_doc[5].find("td[4]")])

    return routes_doc, containers_doc


def get_routes(routes_doc):

    routes = []
    for index, route in enumerate(routes_doc):
        if index > -1:
            route_td = route.getchildren()
            vessel_part1, vessel_part2, voyage = route_td[4].text.strip().split(" ")[:3]
            routes.append({
                'route_name': 'Load Port',
                'location': route_td[5].text.strip(),
                'vessel': "{0} {1}".format(vessel_part1, vessel_part2),
                'voyage': voyage.strip(),
                'call_sign': '',
                'estimate_arrival_date': '',
                'actual_arrival_date': '',
                'container_load_date': route_td[7].text.strip(),
                'container_discharge_date': '',
                'estimate_departure_date': '',
                'actual_departure_date': ''
            })
            routes.append({
                'route_name': 'Discharge Port',
                'location': route_td[6].text.strip(),
                'vessel': "{0} {1}".format(vessel_part1, vessel_part2),
                'voyage': voyage.strip(),
                'call_sign': '',
                'estimate_arrival_date': '',
                'actual_arrival_date': '',
                'container_load_date': '',
                'container_discharge_date': '',
                'estimate_departure_date': '',
                'actual_departure_date': ''
            })
    return routes


def get_containers(containers_doc):
    containers = []
    for index, container in enumerate(containers_doc):
        if index > 1:
            container_td = container.getchildren()
            containers.append({
                'number': container_td[0].find("a").text.strip(),
                'seal_no': container_td[2].text.strip(),
                'status': container_td[7].text.strip(),
                'type': container_td[1].find("span").text[4:6],
                'size': container_td[1].find("span").text[:2],
                'height': '',
                'location': '',
                'container_load_date': '',
                'container_discharge_date': container_td[8].text
            })
    return containers
