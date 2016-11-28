# coding: utf-8

import requests
from app.util.ocr import orc_response
from lxml import etree
import simplejson as json


def grab(bl_num='9735064274801'):
    session = requests.session()

    session.get("http://www.11183.com.cn/mailtracking/you_jian_cha_xun.html")
    code_response = session.get("http://www.11183.com.cn/ems/rand")
    captcha_num = orc_response(code_response)

    print captcha_num

    data = {
        'muMailNum': str.strip(bl_num),
        'checkCode': str.strip(captcha_num.replace(' ', ''))
    }
    response = session.post("http://www.11183.com.cn/ems/order/multiQuery_tn", data=data)
    # print(response.text)
    infos = []
    if response.status_code == 200:
        ems_doc = etree.HTML(unicode.encode(response.text, encoding='utf-8'))
        contents = ems_doc.xpath("//table[@class='showTable']/tr")
        # print(contents)
        pre_process_date = ''
        for content in contents:
            td_elements = content.getchildren()
            infos.append({
                'process_date': td_elements[0].text.strip() if td_elements[0].text else pre_process_date,
                'process_time': td_elements[1].text.strip(),
                'status': u'{0};{1}'.format(td_elements[2].find('div/a').text, td_elements[2].find('div/a').tail) if td_elements[2].text.strip() == '' else td_elements[2].text.strip(),
                'local': td_elements[3].text.strip()
            })
            if td_elements[0].text:
                pre_process_date = td_elements[0].text.strip()

        infos.reverse()
    return infos


if __name__ == '__main__':
    grab()






