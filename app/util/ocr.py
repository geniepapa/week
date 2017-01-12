# coding: utf-8

import os
import subprocess
import urllib2
import cv2
import numpy as np


def get_image(path, url):
    response = urllib2.urlopen(url)
    img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
    img_grep = cv2.imdecode(img_array, 0)

    img_threshold = cv2.threshold(img_grep, 157, 255, cv2.THRESH_BINARY)[1]
    img_denoising = cv2.fastNlMeansDenoising(img_threshold, None, 65, 5, 100)

    img_threshold_second = cv2.threshold(img_denoising, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    img_denoising_second = cv2.fastNlMeansDenoising(img_threshold_second, None, 65, 5, 50)

    cv2.imwrite(path, img_denoising_second)


def get_image_batch(path, url):

    for i in range(1000):
        get_image(path+'/'+str(i+255)+'.png', url)


def get_image_raw(path, url):

    response = urllib2.urlopen(url)
    img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
    img_grep = cv2.imdecode(img_array, 0)

    '''腐蚀'''
    kernel = np.ones((4, 4), np.uint8)
    img_erode = cv2.erode(img_grep, kernel)

    '''二值化'''
    img_threshold = cv2.threshold(img_erode, 1, 255, cv2.THRESH_BINARY)[1]

    cv2.imwrite(path, img_threshold)


def get_image_from_response(path, response):
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img_grep = cv2.imdecode(img_array, 0)
    img = cv2.threshold(img_grep, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite(path, img)


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


def ocr(url):
    image = "captcha.png"
    result = ''
    times = 10
    while len(result) != 5 and --times > 0:
        get_image_raw(image, url)
        '''lang=maersk'''
        result = image_to_string(image)
        result.replace(' ', '').strip()
    return result


def ocr_response(response):
    image = "captcha.png"
    get_image_from_response(image, response)
    result = image_to_string(image)

    result.replace(' ', '')
    return result


def ocr_url(url):
    image = "captcha.png"
    # result = ''
    # times = 10
    # while len(result) != 5 and --times > 0:

    response = urllib2.urlopen(url)
    img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
    img_grep = cv2.imdecode(img_array, 0)

    img_grep[:2, :] = 255
    img_grep[29:, :] = 255
    img_grep[:, :4] = 255
    img_grep[:, 86:] = 255

    img_threshold = cv2.threshold(img_grep, 128, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(image, img_threshold)

    result = image_to_string(image)
    result.replace(' ', '').strip()



    print result

    return result

if __name__ == '__main__':
   capatch = ocr_url("http://www.qingdao-port.net/market/getKaptchaImage.do?timestamp=1484223010551")

