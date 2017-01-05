from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from lxml import etree


def grab(bl_num='MSCUOL252100'):
    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.get("https://www.msc.com/track-a-shipment?agencyPath=chn")

    elem_input = driver.find_element_by_id("ctl00_ctl00_plcMain_plcMain_TrackSearch_txtBolSearch_TextField")
    elem_input.send_keys(str.strip(bl_num))

    driver.execute_script("WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions('ctl00$ctl00$plcMain$plcMain$TrackSearch$hlkSearch', '', true, 'BolSearchPage', '', false, true))")

    elem_output = WebDriverWait(driver, 10).\
        until(ec.presence_of_element_located((By.ID, "ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_pnlBOLContent")))

    print(elem_output.get_attribute("innerHTML"))
    info = html_parse(elem_output.get_attribute("innerHTML"))

    driver.close()

    return info


def html_parse(response):

    routes_doc, containers_doc = get_docs(response)
    return {'routing': get_routes(routes_doc), 'containers': get_containers(containers_doc)}

container_xpath = "//dl[@class='containerAccordion']//dd"
routes_xpath = "//table[1]//tr"


def get_docs(content):

    doc = etree.HTML(unicode.encode(content, encoding='utf-8'))
    containers_doc = doc.xpath(container_xpath)
    routes_doc = doc.xpath(routes_xpath)
    return routes_doc, containers_doc


def get_routes(routes_doc):

    routes = []
    for index, route in enumerate(routes_doc):
        if index == 1:
            route_td = route.getchildren()
            routes.append({
                'route_name': 'Load Port',
                'location': route_td[2].find('span').text.strip(),
                'vessel': route_td[1].find('span').text.strip(),
                'voyage': '',
                'call_sign': '',
                'estimate_arrival_date': '',
                'actual_arrival_date': '',
                'container_load_date': '',
                'container_discharge_date': '',
                'estimate_departure_date': route_td[0].find('span').text.strip(),
                'actual_departure_date': ''
            })
        if index == 3:
            route_td = route.getchildren()
            routes.append({
                'route_name': 'Discharge Port',
                'location': route_td[0].find('span').text.strip(),
                'vessel': '',
                'voyage': '',
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

        containers.append({
            'number':  container.find('a').text,
            'seal_no': '',
            'status': '',
            'type': container.find('div/table/tbody[1]/tr/td[1]/span').text.strip()[3:],
            'size': container.find('div/table/tbody[1]/tr/td[1]/span').text.strip()[:2],
            'height': '',
            'location': container.find('div/table/tbody[1]/tr/td[2]/span').text.strip(),
            'container_load_date': '',
            'container_discharge_date': ''
        })
    return containers


if __name__ == '__main__':
    grab()
