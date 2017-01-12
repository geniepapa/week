import requests
from lxml import etree

session_url = "http://homeport.apl.com/gentrack/trackingMain.do"
content_url = "http://homeport.apl.com/gentrack/blRoutingFrame.do"


def grab(bl_num='086422833'):
    session = requests.session()
    session.get(session_url, params={'trackInput01': str.strip(bl_num)})
    response = session.get(content_url)

    # return response.text
    infos = []
    if response.status_code == 200:
        apl_doc = etree.HTML(unicode.encode(response.text, encoding='utf-8'))
        routes_doc = apl_doc.xpath("//form/table[1]//tr")
        containers_doc = apl_doc.xpath("//div[@id='pnlGrid']/table//tr")
        routes = []
        containers = []
        for index, route in enumerate(routes_doc):
            if index > 0:
                route_td = route.getchildren()
                vessel_and_voyage = route_td[3].getchildren()[2].text.strip()
                ship, vessel, voyage = ['', '', '']
                if vessel_and_voyage:
                    ship, vessel, voyage = vessel_and_voyage.split(' ')

                arrival_date = route_td[4].text.strip()
                departure_date = route_td[5].text.strip()

                if route_td[1].text.strip() in ['Load Port', 'Discharge Port']:
                    routes.append({
                        'route_name': route_td[1].text.strip(),
                        'location': route_td[2].getchildren()[0].text.strip(),
                        'vessel': '{0} {1}'.format(ship, vessel),
                        'voyage': voyage,
                        'estimate_arrival_date': arrival_date[-1] in ['P', 'E'] and arrival_date[0:-2] or '',
                        'actual_arrival_date': arrival_date[-1] == 'A' and arrival_date[0:-2] or '',
                        'container_discharge_date': arrival_date[-1] == 'D' and arrival_date[0:-2] or '',
                        'container_load_date': departure_date[-1] == 'L' and departure_date[0:-2] or '',
                        'estimate_departure_date':  departure_date[-1] in ['P', 'E'] and departure_date[0:-2] or '',
                        'actual_departure_date':  departure_date[-1] == 'A' and departure_date[0:-2] or '',
                    })
        for index, container in enumerate(containers_doc):
            if index > 0:
                container_td = container.getchildren()
                containers.append({
                    'number': container_td[0].text.strip(),
                    'status': container_td[7].text.strip(),
                    'type': container_td[1].text.strip(),
                    'size': container_td[2].text.strip(),
                    'height': container_td[3].text.strip(),
                    'location': container_td[8].text.strip(),
                    'container_load_date': '',
                    'container_discharge_date': ''
                })

        infos = {
            'routing': routes,
            'containers': containers
        }

    return infos
