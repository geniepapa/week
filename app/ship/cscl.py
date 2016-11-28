import requests

session_url = "http://222.66.158.204/cargo_track/"
content_url = "http://222.66.158.204/cargo_track/cargo_track_rst.jsp"


def grab(bl_num='SHANGO042447'):
    session = requests.session()
    data = {
        'tr_num': 'bl_no',
        'tf_bl_no':  str.strip(bl_num),
        'submit\"2': 'O K',
        'lang': 'EN'
    }
    session.get(session_url)
    response = session.post(content_url, data=data)
    return response.text
