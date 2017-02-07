import requests
from lxml import etree

content_url = "http://ebusiness.coscon.com/NewEBWeb/public/cargoTracking/cargoTracking.xhtml"

routes_xpath = "//table[@id='actualLoadingInfo']/tbody/tr"
container_xpath = "//table[@id='cargoTrackingContainerInfoStatus']/tbody/tr"


def grab(bl_num='8013296880'):
    session = requests.session()

    headers = {'Faces-Request': 'partial/ajax'}

    data = {
        'mainForm': 'mainForm',
        'cargoTrackSearchId': 'BILLOFLADING',
        'cargoTrackingPara': str.strip(bl_num),
        'javax.faces.ViewState': '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',
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'cargoTrckingFindButton',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': 'bookingNumbers billToBookingGrop billofLading_Table3 release_Information_bill release_Information_booking cargoTrackingOrderBillInformation cargoTrackingBookingOfLadingInformation cargoTrackingContainerHistory cargoTrackingContainerInfoStatus cargoTrackingContainerBillOfLadingNumber1 cargoTrackingContainerInfoByContainerNumber release_Information_booking_version release_Information_bill_version actualLoadingInfo containerInfoByBlNum containerInfoByBkgNumTable actualLoadingInfo5 documentStatus cargoTrackingAcivePictures containerNumberAll containerInfo_table3 containerInfo_table4 cargoTrackingPrintByContainer containerNumberAllByBookingNumber registerUserValidate validateCargoTracking isbillOfLadingExist isbookingNumberExist cargoTrackingContainerPictureByContainer cargoTrackingContainerHistory1 cargoTrackingOrderBillMyFocus cargoTrackingBookingMyFocus userId contaienrNoExist billChange4 bookingChange4 bookingChange3 cargoTrackingContainerHistory6 numberType containerSize containerMessage containerTab isLogin cargoTrackingBillContainer cargoTrackingBillContainer1 BillMessage BookingMessage searchSuccess searchError containerTransportationMode',
        'cargoTrckingFindButton': 'cargoTrckingFindButton'
    }

    response = session.post(content_url, data=data, headers=headers)

    # print response.text

    if response.status_code == 200:
        return html_parse(response)

    return None


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
    for route in routes_doc:
        route_td = route.getchildren()
        routes.append({
            'route_name': 'Load Port',
            'location': route_td[2].getchildren()[0].text.strip(),
            'vessel': route_td[0].getchildren()[0].text.strip(),
            'voyage': route_td[1].getchildren()[0].text.strip(),
            'call_sign': '',
            'estimate_arrival_date': '',
            'actual_arrival_date': '',
            'container_load_date': '',
            'container_discharge_date': '',
            'estimate_departure_date': route_td[4].getchildren()[0].text.strip(),
            'actual_departure_date': route_td[5].getchildren()[0].text.strip()
        })
        routes.append({
            'route_name': 'Discharge Port',
            'location': route_td[6].getchildren()[0].text.strip(),
            'vessel': route_td[0].getchildren()[0].text.strip(),
            'voyage': route_td[1].getchildren()[0].text.strip(),
            'call_sign': '',
            'estimate_arrival_date': route_td[7].getchildren()[0].text.strip(),
            'actual_arrival_date': route_td[8].getchildren()[0].text,
            'container_load_date': '',
            'container_discharge_date': '',
            'estimate_departure_date': '',
            'actual_departure_date': ''
        })
    return routes

def get_containers(containers_doc):
    containers = []
    for container in containers_doc:
        container_td = container.getchildren()
        containers.append({
            'number': container_td[1].find("div/a").attrib["title"],
            'seal_no': container_td[3].find("div/span").text,
            'status': container_td[5].find("div/span").text,
            'type': container_td[2].find("div/span").text[2:],
            'size': container_td[2].find("div/span").text[:2],
            'height': '',
            'location': container_td[4].find("div/span").text,
            'container_load_date': '',
            'container_discharge_date': container_td[6].find("div/span").text
        })
    return containers






