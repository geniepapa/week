
import requests
from app.util.ocr import image_to_string
from lxml import etree
from PIL import Image
import cStringIO
import io


def grab(bl_num='PASU5136409630'):

    session = requests.session()
    session.get("http://www.yydy.com/dyxt/BasicService/CheckLogin.aspx?oper=UserLogin_New&name=CARGO&pwd=000000")
    session.get("http://www.yydy.com/dyxt/index.aspx")
    captcha_response = session.get("http://www.yydy.com/dyxt/BasicService/CreateCheckCode.aspx")
    captcha = image_to_string(get_image_from_response("yydy.png", captcha_response))
    print(captcha)
    session.get("http://www.yydy.com/dyxt/BasicService/QueryService.aspx?oper=QueryByBill&param="+bl_num+"&CheckCode="+captcha)
    response = session.get("http://www.yydy.com/dyxt/Query/ExportByBill.aspx?s_no="+bl_num)
    # html = etree.HTML(unicode.encode(response.text, encoding='utf-8'))

    html = etree.HTML(response.text)
    info_html = html.xpath("//form/div")

    if len(info_html) > 1:
        info = etree.tostring(info_html[1], pretty_print=True)
    else:
        info = None
    session.close()

    return info


def get_image_from_response(path, response):

    image = Image.open(cStringIO.StringIO(response.content))
    buf = cStringIO.StringIO()
    image.save(buf, format="PNG")

    image_png = Image.open(buf)
    image_grep = image_png.convert("L")

    threshold = 168
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image_threshold = image_grep.point(table, "1")

    image_threshold.save(path)

    return path

if __name__ == '__main__':
    grab()
