# coding: utf-8

import os
import subprocess
import urllib2
import cv2
import numpy as np
from PIL import Image


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

def get_image_by_color(path):

    image = cv2.imread("5.png")
    # 去背景
    for i, row in enumerate(image):
        for j, cell in enumerate(row):
            if (image[0, 1] == image[i, j]).all() or (image[34, 1] == image[i, j]).all():
                if (i == 0 and j == 1) or (i == 34 and j == 1):
                    continue
                image[i, j] = [255, 255, 255]

    # 转换HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 去掉其他颜色
    for i, row in enumerate(hsv):
        for j, cell in enumerate(row):
            if image[i, j][0] >= 200:
                pass
            else:
                hsv[i, j] = [0, 0, 255]

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 腐蚀
    kernel = np.ones((1, 2), np.uint8)
    img_erode = cv2.erode(img, kernel)
    # 灰度
    gray = cv2.cvtColor(img_erode, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    kernel = np.ones((2, 1), np.uint8)
    img_erode2 = cv2.dilate(binary, kernel)

    # 反色

    for i, row in enumerate(img_erode2):
        for j, cell in enumerate(row):
            img_erode2[i, j] = 255 - img_erode2[i, j]
    for j in range(89):
        for i in range(34/2):
            if img_erode2[i+1, j] == 0:
                img_erode2[i, j] = 255
                img_erode2[i + 1, j] = 255
            else:
                break
        for i in range(34 / 2):
            if img_erode2[34 - i - 1, j] == 0:
                img_erode2[34 - i, j] = 255
                img_erode2[34 - i - 1, j] = 255
            else:
                break
    '''
    kernel = np.ones((2, 2), np.uint8)
    img_erode3 = cv2.erode(img_erode2, kernel)

    kernel = np.ones((2, 2), np.uint8)
    img_erode4 = cv2.dilate(img_erode3, kernel)

    kernel = np.ones((2, 2), np.uint8)
    img_erode5 = cv2.erode(img_erode4, kernel)

    kernel = np.ones((2, 2), np.uint8)
    img_erode6 = cv2.dilate(img_erode5, kernel)
    '''

    '''
    for i, row in enumerate(img_erode2):
        for j, cell in enumerate(row):
            if i < 34 and j < 89 and \
                            img_erode2[i, j] == 0 and img_erode2[i+1, j] == 0 and \
                            img_erode2[i, j+1] == 0 and img_erode2[i+1, j+1] == 0:
                img_erode2[i, j] = 255
    '''


    # 轮廓
    # contours = cv2.findContours(img_erode2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img_erode2, contours[1], -1, (255, 255, 255), 1)

    '''
        kernel = np.ones((2, 2), np.uint8)
        img_erode2 = cv2.erode(binary, kernel)


        # 轮廓
        contours = cv2.findContours(img_erode2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        result_image = cv2.drawContours(binary, contours[1], -1, (0, 0, 255), 1)

        cv2.imwrite("2.png", img_erode2)

        # image_to_string("3.png", lang="chi_sim")
        # print result
    '''
    cv2.imwrite("2.png", img_erode2)
    image_to_string("2.png")
    cv2.imshow('image', img_erode2)
    cv2.waitKey(0)




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
    result = image_to_string("2.png")
    print result

