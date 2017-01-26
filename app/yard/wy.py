# coding: utf-8

import requests
from lxml import etree


def grab(bl_num='WDFCNIY17052002'):

    session = requests.session()

    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': 'QtrBR5fuv4RNb1Q4soPgCNn6PH6jBt9ZKhkGkjMqvew74Nsmg6d65D6Iol1Wchp/wz2wsIUW5yenc1g9rNA4ZJx6Y11/Dz1I+qNOevdT/6yHNBbAEisRclLY9kZhnDBUKjY0ckBQ9QaR3tdrvVkh4Zt27189GyxII5xwb3fNITRXleElPaY2coqilIRRqcbjaazyRXyOb4/6G5TNnDB6Yp41DroLVHLho7Qcm3fVMksve/i4wH9G1bbqYPCeAT6eaTm0q0f9zuOPn3HXuqHdq7TrYHkNnXWqYnpa0G5ZbFWbM4sPdoqp325XW7wblZLnkjGLr0/4roTjYh9CVD+mj6t9Ev9NS0PkMZHaw10BajYvqDDYXIfUsE61Zu+JgnqnVbKdYYMjeojnMa0aTzXRqiOREDxfsspliKJDCpGR7t+0B1a2cBf5jWelvESQNJawUdhz8yKtYS9TGotRvNJ6tnBJgnb0JrENNtYFz8mLqoYseXCQFl+O4Jb8C8eaYlJHEIJtM3gZ82QlqM9s0OkAglVZUrjly8XMSquq8KbpikqPJA3bDJkFF7evGqfpl0CqHybLVHqUdaHjSaPNypGT4Pci2KEfTNcQw3HbMY6Cb03W7Lz+dVBP6gTjGQ5SCYaXI0OFK6TxLLripYc2kiSa8QuWzSCieExBMvjz63QkgdMQtnw0T9cFCakQeLskmLuzW4BJSI1uaUVo48nRu+1ecVlB9g8cFfvstQQOf3oqjMwfwFbaYbgcGxLTYl7jcVhIAd6JJIhaG3rUTFhw4BeA2zqK+A5WGeywHe4YoP914sE79/oL3G937tW9I8UFdHNXTWM5av6ZDAveuOB7ADOS7iAR5C8ajineGQ3jAqJAGuPj+bTzMTUjFh10HIPmsXDCFP2OZIduWQiqnuZ40LxpdWtzE1NlQpZmzjwcPlfPdVvrsyTu6tWS3+EJMWaHkqV8KPz7ZpSyCN+cvaNXT24OgMj46BLlWoJQQyWsSYU49c75J9IgxNWAaRHqsgReKnCAlZejiVet/ssLHciWKQINY1lJljLvKfMI5ZLlO8HIDhg4u3lY1jwHFJSk3KYEkwa+J0S4A/As1Z2ueR9TRyi1XpUz/meBZtj8PPuowyUodOK3muD28j2nLipOU5zZvR9B5OQdZ7KVQ90JdqmpMEFNlLNVEJZVLW6ph0U8JNGO5eO2ThTcesuJ+EEaZp6RvTq1NG3DjrdeELyaY9ZU0l+9tSN9OYUPwWuAQea6guGI7GS4bqDEET1OPYqYVEJtHruUut72owdRLwuuBFLwLrvsgkSKISB0szuUYzB1FV5SLqvgzQ1SzBTQQ0pEbNdI3uDKWpNXb1xT12UK7uUTiVRNDhL16Tx3J6S9a7oHwHWi02ZZCXPaQCkl0KepPXXoxGCWUfvRukkwbkKDnTa8akTQCvSvYPbZIxtmb/emqrDW0Bncv/KrB+dmSm+ifDhJGVkX6Zx3VueNLdnL1x+MR9Y8dgvLpA185kAiJ4nvfv4HkQTYCfeU+BOn36Kv75w3X7ZB9z3Z7jPVQB7X05mcSRA5vAZyiIHY0wX44yVT36DJUoFa79LOugnMlINur/fzMNE0y+epTcDVdqzCFwAEkzE8BhuJs5LKOpT25Ck7TtvoFSNiDL+r3zH2VNx8BZSFEKPZ647erwkkk39lN0pMIBh/stVc62e6M5+sp8fSdbnsyklklRts8Mw/CgbXciz5qWn1+G0ov4jqR8MSJmwtv6lJyZ0bp9glTBo/pw/Z7zxYXQflkyiu9LGn9713obu2OlJZgow8Yw==',
        '__VIEWSTATEGENERATOR': '73AAD272',
        '__VIEWSTATEENCRYPTED': '',
        '__PREVIOUSPAGE': '39Czbhz0EcTlF7IcU1z1smpQkJIO4SkIaV4WMz8CiyOFpIMiyvHiJ608uRZYIswRwS-AgQTrjfN-NJ1Yn0ZC8PaqlN4hkmoJXRhm-JJUuhB6yj7vbE2LfoQ25LW5reRJFdULzA2',
        'txtBlno': bl_num.strip(),
        'rbBlnoType': u'主单号',
        'btnQuery': u'查询'
    }
    response = session.post("http://www.sd.sinotrans.com/sdweb/HomePage/CntrYardQuery/QueryByBlno.aspx", data=data)

    html = etree.HTML(response.text)

    # html = etree.HTML(response.text)

    info_html = html.xpath("//body/form/table[3]")

    if len(info_html) > 0:

        elem_links = info_html[0].xpath("//a")
        for elem_link in elem_links:
            elem_link.set("href", "#")

        info = etree.tostring(info_html[0], pretty_print=True)
    else:
        info = None
    session.close()

    return info


if __name__ == '__main__':
    grab()
