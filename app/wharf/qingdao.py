# coding: utf-8

import os
import subprocess
import requests
import cv2
import numpy as np

import simplejson as json


qingdao_session = requests.session()


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


def grab_ship(vessel='JI HAI ZHI XING', voyage='15007N'):
    url = "http://track.qingdao-port.net/dccx"
    query = "http://track.qingdao-port.net/logistics/singleship/querySingleShip?YWCM=" + vessel + "&CKHC=" + voyage
    return search(url, query)


def grab_bill(port_type='NONE', bill_type='ZTDH', bill='PASU5136190180'):
    url = "http://track.qingdao-port.net/wmdp"
    query = "http://track.qingdao-port.net/logistics/wmdp/queryWmdp?tdhType="+bill_type+"&jckType="+port_type+"&value="+bill
    return search(url, query)




def search(url, query):
    result = None

    # session = requests.session()
    response = qingdao_session.get(url)

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
                'userName': '18250717925',
                # 'userName': 'geniepapa@gmail.com',
                'passWord': 'Yaitoo.951',
                # 'passWord': 'liuyang_902',
                'code': eval_code
            }

            login_ajax_response = qingdao_session.post("http://www.qingdao-port.net:80/market/login.do", data)

            json_login = json.loads(unicode.encode(login_ajax_response.text, encoding='utf-8'))


            if json_login["success"] == True:
                qingdao_session.get("http://www.qingdao-port.net")
                qingdao_session.get(url)
                result_response = qingdao_session.post(query)
                result = json.loads(unicode.encode(result_response.text, encoding='utf-8'))
                # print unicode.encode(result_response.text, encoding='utf-8')
                qingdao_session.get("http://www.qingdao-port.net/page/logout.do")
                break
            elif len(json_login) > 2:
                print login_ajax_response.text
                result = json_login
                break

    return result

if __name__ == '__main__':
    grab_bill()
