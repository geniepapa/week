# coding: utf-8

import os
import subprocess
import requests
from app.util.ocr import ocr_response
from lxml import etree
from selenium import webdriver
import cv2
import re



def grab_back(vessel='JI HAI ZHI XING', voyage='16094S'):

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

def grab():
    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.get("http://www.qingdao-port.net/common/page/login.jsp")

    elem_input = driver.find_element_by_id("userName")
    elem_input.send_keys('18250717925')


    elem_captcha_url = driver.find_element_by_id("imgObj")
    # url_captcha = elem_captcha_url.get_attribute("src")
    # driver.get(url_captcha)
    driver.save_screenshot('qingdao.png')

    # driver.back()
    # elem_captcha_url.screenshot('qingdao.png')

    elem_password = driver.find_element_by_id("passWord")
    elem_password.send_keys('Yaitoo.951')

    elem_captcha = driver.find_element_by_id("code")
    #elem_captcha_url.click()

    captcha = image_to_string(get_image('qingdao.png'))
    captcha = captcha.replace(' ', '')
    captcha = captcha.replace('\'', '')
    captcha = captcha.replace('\\', '1')
    captcha = captcha.replace('x', '*')
    print captcha

    while re.match(r'[0-9]+[+|\-|*][0-9]+', captcha) is None:
        elem_captcha_url.click()
        driver.save_screenshot('qingdao.png')

        captcha = image_to_string(get_image('qingdao.png'))
        captcha = captcha.replace(' ', '')
        captcha = captcha.replace('\'', '')
        captcha = captcha.replace('\\', '1')
        captcha = captcha.replace('x', '*')
        print captcha

    print eval(captcha)

    elem_captcha.send_keys(eval(captcha))

    elem_submit = driver.find_element_by_id("login")
    elem_submit.click()

    elem_banner = driver.find_element_by_id("top-banner")
    print elem_banner.get_attribute("innerHTML")



    driver.close()

    return None


def get_image(image):

    img_grep = cv2.imread(image, 0)
    crop_img = img_grep[395:425, 975:1060]

    # response = urllib2.urlopen(url)
    # img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
    # img_grep = cv2.imdecode(img_array, 0)

    # 去边框
    crop_img[:2, :] = 255
    crop_img[29:, :] = 255
    crop_img[:, :4] = 255
    crop_img[:, 84:] = 255

    img_threshold = cv2.threshold(crop_img, 128, 255, cv2.THRESH_BINARY)[1]
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



if __name__ == '__main__':
    grab()
