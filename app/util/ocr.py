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


def get_image_from_response(path, response):
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img_grep = cv2.imdecode(img_array, 0)
    img = cv2.threshold(img_grep, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite(path, img)


def image_to_string(img, lang='eng' ,cleanup=True):
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
    get_image(image, url)
    result = image_to_string(image, lang='maersk')
    result.replace(' ', '')
    return result


def orc_response(response):
    image = "captcha.png"
    get_image_from_response(image, response)
    result = image_to_string(image)
    result.replace(' ', '')
    return result


