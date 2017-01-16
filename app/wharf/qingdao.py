# coding: utf-8

import os
import subprocess
import requests
from app.util.ocr import ocr_response
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import cv2
import re
import time
import pprint
import numpy as np

import simplejson as json


qingdao_session = requests.session()

def grab_back(vessel='JI HAI ZHI XING', voyage='15007N'):

    session = requests.session()
    session.get("http://www.qingdaoport.net/ywzx/ship/shipcx.jsp")

    captcha_response = session.get("http://www.qingdaoport.net/adv/random.jsp")
    captcha = ocr_response(captcha_response)

    print(captcha)

    response = session.post("http://www.qingdaoport.net/ywzx/ship/shipcx.jsp", data={
        'vessel_name': vessel,
        'voyage_number': voyage,
        'num': captcha})

    # html = etree.HTML(unicode.encode(response.text, encoding='utf-8'))
    html = etree.HTML(response.text)
    session.close()

    info = []

    columns = html.xpath('//table')[7][2].getchildren()

    if columns and len(columns) > 2:
        info.append({
            'status': columns[8].text,
            'wharf': columns[0].find('b').text,
            'local': columns[15].text,
            'ship': columns[6].text,
            'eta': columns[9].text,
            'ata': columns[10].text,
            'etd': columns[11].text,
            'atd': columns[12].text,
            'piling': columns[13].text,
            'unpiling': columns[14].text
        })

    return info

def grab_webdriver():

    driver = webdriver.PhantomJS()
    login_url = 'http://www.qingdao-port.net/common/page/login.jsp'
    search_url = 'http://track.qingdao-port.net/dccx'
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.get(search_url)

    if driver.current_url == login_url:
        login(driver, login_url)
        driver.get(search_url)

    driver.save_screenshot('success.png')
    driver.close()

    return None


def get_image(response):

    image = "qingdao.png"
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img_grep = cv2.imdecode(img_array, 0)

    #img_grep = cv2.imread(image, 0)
    #crop_img = img_grep[395:425, 975:1060]
    #crop_img = img_grep[590:635, 1510:1635]

    # 去边框
    img_grep[:2, :] = 255
    img_grep[29:, :] = 255
    img_grep[:, :4] = 255
    img_grep[:, 84:] = 255

    img_threshold = cv2.threshold(img_grep, 128, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(image, img_threshold)

    return image


def image_to_string(img, lang='eng', cleanup=True):
    subprocess.check_output('tesseract ' + img + ' ' + img + ' -l '+lang+' ',
                            stderr=subprocess.STDOUT,
                            shell=True)
    text = ''
    with open(img + '.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text

def login(driver, url):

    driver.get(url)

    elem_input = driver.find_element_by_id("userName")
    elem_input.send_keys('18250717925')

    elem_password = driver.find_element_by_id("passWord")
    elem_password.send_keys('Yaitoo.951')

    elem_captcha = driver.find_element_by_id("code")
    elem_submit = driver.find_element_by_id("login")

    driver.save_screenshot('qingdao.png')
    captcha = image_to_string(get_image('qingdao.png'))
    captcha = captcha.replace(' ', '').replace('\'', '').replace('‘','').\
        replace('A', '4').replace('?', '7').replace('\\', '1').replace('x', '*').strip()

    print captcha

    elem_captcha.send_keys(eval(captcha))
    elem_submit.click()

    time.sleep(10)
    driver.save_screenshot('login.png')


def grab_ship(vessel='JI HAI ZHI XING', voyage='15007N'):

    result = None

    # session = requests.session()
    response = qingdao_session.get("http://track.qingdao-port.net/dccx")

    if response.url == "http://www.qingdao-port.net/common/page/login.jsp":

        while True:
            captcha_response = qingdao_session.get("http://www.qingdao-port.net:80/market/getKaptchaImage.do")
            code = image_to_string(get_image(captcha_response))
            code = code.replace(' ', '').replace('\'', '').replace('‘', ''). \
                replace('A', '4').replace('?', '7').replace('\\', '1').replace('x', '*').strip()

            try:
                eval_code = eval(code)
            except:
                eval_code = 0

            data = {
                #  'userName': '18250717925',
                'userName': 'geniepapa@gmail.com',
                # 'passWord': 'Yaitoo.951',
                'passWord': 'liuyang_902',
                'code': eval_code
            }


            login_ajax_response = qingdao_session.post("http://www.qingdao-port.net:80/market/login.do", data)
            json_login = json.loads(login_ajax_response.text)

            if json_login["success"] == True:
                location_href_response = qingdao_session.get("http://www.qingdao-port.net")

                get_track_response = qingdao_session.get("http://track.qingdao-port.net/dccx")
                get_tips_response = qingdao_session.post(
                    "http://track.qingdao-port.net/logistics/sxjh/query/tips?YWCM=JI HAI ZHI XING")
                result_response = qingdao_session.post(
                    "http://track.qingdao-port.net/logistics/singleship/querySingleShip?YWCM=" + vessel + "&CKHC=" + voyage)

                result = json.loads(result_response.text)

                qingdao_session.get("http://www.qingdao-port.net/page/logout.do")

                break
            elif len(json_login) > 2:
                print login_ajax_response.text
                result = json_login
                break

    return result


def grab_bill(bill='PASU5136190180'):
    result = None

    # session = requests.session()
    response = qingdao_session.get("http://track.qingdao-port.net/wmdp")

    if response.url == "http://www.qingdao-port.net/common/page/login.jsp":

        while True:
            captcha_response = qingdao_session.get("http://www.qingdao-port.net:80/market/getKaptchaImage.do")
            code = image_to_string(get_image(captcha_response))
            code = code.replace(' ', '').replace('\'', '').replace('‘', ''). \
                replace('A', '4').replace('?', '7').replace('\\', '1').replace('x', '*').strip()

            try:
                eval_code = eval(code)
            except:
                eval_code = 0

            data = {
                #  'userName': '18250717925',
                'userName': 'geniepapa@gmail.com',
                # 'passWord': 'Yaitoo.951',
                'passWord': 'liuyang_902',
                'code': eval_code
            }

            login_ajax_response = qingdao_session.post("http://www.qingdao-port.net:80/market/login.do", data)
            json_login = json.loads(login_ajax_response.text)

            if json_login["success"] == True:
                location_href_response = qingdao_session.get("http://www.qingdao-port.net")

                get_track_response = qingdao_session.get("http://track.qingdao-port.net/wmdp")

                result_response = qingdao_session.post(
                    "http://track.qingdao-port.net/logistics/wmdp/queryWmdp?tdhType=ZTDH&jckType=NONE&value="+bill)

                result = json.loads(result_response.text)

                qingdao_session.get("http://www.qingdao-port.net/page/logout.do")

                break
            elif len(json_login) > 2:
                print login_ajax_response.text
                result = json_login
                break

    return result

def

if __name__ == '__main__':
    grab_bill()
