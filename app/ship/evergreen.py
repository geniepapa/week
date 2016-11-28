import requests

#session_url = "http://www.shipmentlink.com/servlet/TDB1_CargoTracking.do"
content_url = "http://www.shipmentlink.com/servlet/TDB1_CargoTracking.do"


def grab(bl_num='003602132872'):
    session = requests.session()
    data = {
        'BL':  str.strip(bl_num),
        'TYPE': 'BL',
        'SEL': 's_bl',
        'NO': str.strip(bl_num)
    }
    session.get(content_url)
    response = session.post(content_url, params=data)
    return response.text
