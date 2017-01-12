# coding: utf-8


from selenium import webdriver
import requests
from app.util.ocr import orc_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from lxml import etree

base_path = 'https://my.maerskline.com'

def grab(bl_num='958586127'):

    info = None

    driver = webdriver.Chrome()
    # driver = webdriver.PhantomJS()
    driver.get(base_path+'/tracking/search')

    elem_input = driver.find_element_by_id("searchNumber")
    elem_input.send_keys(str.strip(bl_num))

    elem_captcha = driver.find_element_by_id("randomID")
    captcha_num = orc_url(base_path + '/captchaapp/captcha?id=' + elem_captcha.get_attribute("value"))

    print captcha_num
    elem_code = driver.find_element_by_id("code")
    elem_code.send_keys(str.strip(captcha_num))


    elem_submit = driver.find_element_by_id("trackingUnregistered")
    # elem_submit.click()









    # driver.close()

    return info


def html_parse(response):

    routes_doc, containers_doc = get_docs(response)
    return {'routing': get_routes(routes_doc), 'containers': get_containers(containers_doc)}

container_xpath = ""
routes_xpath = ""


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
                'location': '',
                'vessel': '',
                'voyage': '',
                'call_sign': '',
                'estimate_arrival_date': '',
                'actual_arrival_date': '',
                'container_load_date': '',
                'container_discharge_date': '',
                'estimate_departure_date':'',
                'actual_departure_date': ''
            })
        if index == 3:
            route_td = route.getchildren()
            routes.append({
                'route_name': 'Discharge Port',
                'location': '',
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
            'number':  '',
            'seal_no': '',
            'status': '',
            'type': '',
            'size': '',
            'height': '',
            'location': '',
            'container_load_date': '',
            'container_discharge_date': ''
        })
    return containers


if __name__ == '__main__':
    grab()
