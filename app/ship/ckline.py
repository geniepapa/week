import requests
from lxml import etree

content_url = "http://www.ckline.co.kr/korea/service/se03.ck"


def grab(bl_num='CKCOSUB1600737'):
    session = requests.session()
    data = {'cmd': 'se', 'subCmd': '03', 'lastCmd': '05', 'select_Gubun': 'sbkg_bl', 'user_bkg_bl': bl_num}
    response = session.post(content_url, data=data)

    infos = None
    if response.status_code == 200:
        ckline_doc = etree.HTML(unicode.encode(response.text, encoding='utf-8'))

        routes_doc = ckline_doc.xpath("//table[@class='box_s'][2]/tr")
        containers_doc = ckline_doc.xpath("//table[@class='box_s'][1]/tr[2]/td[1]")[0]

        routes = []
        containers = []

        route_td = routes_doc[1].getchildren()
        route_td.extend(routes_doc[4].getchildren())

        routes.append({
            'route_name': 'Load Port',
            'location': route_td[6].text.strip(),
            'vessel': route_td[1].text.strip(),
            'voyage': route_td[0].text.strip(),
            'call_sign': route_td[2].text.strip(),
            'estimate_arrival_date': route_td[7].text.strip(),
            'actual_arrival_date':  '',
            'container_load_date': '',
            'container_discharge_date': '',
            'estimate_departure_date': '',
            'actual_departure_date': ''
        })
        routes.append({
            'route_name': 'Discharge Port',
            'location': route_td[9].text.strip(),
            'vessel': route_td[1].text.strip(),
            'voyage': route_td[0].text.strip(),
            'call_sign': route_td[2].text.strip(),

            'estimate_arrival_date': '',
            'actual_arrival_date': '',
            'container_load_date': '',
            'container_discharge_date': '',
            'estimate_departure_date': route_td[10].text.strip(),
            'actual_departure_date': ''
        })

        container_no, seal_no = containers_doc.text.strip().split('/')

        containers.append({
            'number': container_no[5:],
            'status': '',
            'type': container_no[2:4],
            'size': container_no[:2],
            'height': '',
            'location': '',
            'container_load_date': '',
            'container_discharge_date': ''
        })
        for container in containers_doc.getchildren():
            container_no, seal_no = container.tail.strip().split('/')
            containers.append({
                'number': container_no[5:],
                'status': '',
                'type': container_no[2:4],
                'size': container_no[:2],
                'height': '',
                'location': '',
                'container_load_date': '',
                'container_discharge_date': ''
            })

        infos = {
            'routing': routes,
            'containers': containers
        }

    return infos




