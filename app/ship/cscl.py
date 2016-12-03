import requests
from lxml import etree

session_url = "http://222.66.158.204/cargo_track/"
content_url = "http://222.66.158.204/cargo_track/cargo_track_rst.jsp"

routes_xpath = "//form/center/table/tr/td/table[2]/tr[9]/td/table/tr"
container_xpath = "//form/center/table/tr/td/table[2]/tr[5]/td/table/tr"


def grab(bl_num='SHANGO042447'):
    session = requests.session()
    data = {
        'tr_num': 'bl_no',
        'tf_bl_no':  str.strip(bl_num),
        'submit\"2': 'O K',
        'lang': 'EN'
    }
    session.get(session_url)
    response = session.post(content_url, data=data)

    return html_parse(response)


def html_parse(response):

    routes_doc, containers_doc = get_docs(response.text)
    return {'routing': get_routes(routes_doc), 'containers': get_containers(containers_doc)}


def get_docs(content):

    doc = etree.HTML(unicode.encode(content, encoding='utf-8'))
    containers_doc = doc.xpath(container_xpath)
    routes_doc = doc.xpath(routes_xpath)

    return routes_doc, containers_doc


def get_routes(routes_doc):

    routes = []
    for index, route in enumerate(routes_doc):
        if index > 0:
            route_td = route.getchildren()
            routes.append({
                'route_name': 'Load Port',
                'location': route_td[1].find("div/font").text.strip(),
                'vessel': route_td[0].find("div/font/a").text.strip(),
                'voyage': route_td[0].find("div/font/a/br").tail.strip(),
                'call_sign': '',
                'estimate_arrival_date': '',
                'actual_arrival_date': '',
                'container_load_date': '',
                'container_discharge_date': '',
                'estimate_departure_date': route_td[2].find("div/font").text.strip(),
                'actual_departure_date':''
            })
            routes.append({
                'route_name': 'Discharge Port',
                'location': route_td[3].find("div/font").text.strip(),
                'vessel': route_td[0].find("div/font/a").text.strip(),
                'voyage': route_td[0].find("div/font/a/br").tail.strip(),
                'call_sign': '',
                'estimate_arrival_date': route_td[4].find("div/font").text.strip(),
                'actual_arrival_date': '',
                'container_load_date': '',
                'container_discharge_date': '',
                'estimate_departure_date': route_td[5].find("div/font").text.strip(),
                'actual_departure_date': ''
            })
    return routes


def get_containers(containers_doc):
    containers = []
    for index, container in enumerate(containers_doc):
        if index > 0:
            container_td = container.getchildren()
            containers.append({
                'number': container_td[0].find("font/a").text.strip(),
                'seal_no': container_td[1].find("font").text.strip(),
                'status': '',
                'type': container_td[2].find("font").text[2:],
                'size': container_td[2].find("font").text[:2],
                'height': '',
                'location': '',
                'container_load_date': '',
                'container_discharge_date': ''
            })
    return containers


