# coding: utf-8

import requests
from flask import render_template
from lxml import etree

from app.ship import sources as ship_sources
from forms import WharfForm, ShippingForm, ExpressForm
from . import main
from ..express import sources as express_sources
from ..util.ocr import orc_response


@main.route('/', methods=['GET', 'POST'])
def index():
    return wharf()


@main.route('/shipping', methods=['GET', 'POST'])
def shipping():
    form = ShippingForm()
    info = None
    if form.validate_on_submit():
        if form.bill_number.data == '':
            info = ship_sources[form.ship_name.data.encode("utf-8")].grab()
        else:
            info = ship_sources[form.ship_name.data.encode("utf-8")].grab(form.bill_number.data.encode("utf-8"))

    return render_template('shipping.html', form=form, info=info)


@main.route('/wharf', methods=['GET', 'POST'])
def wharf():
    form = WharfForm()
    info = None
    if form.validate_on_submit():

        session = requests.session()
        session.get("http://www.qingdaoport.net/ywzx/ship/shipcx.jsp")

        captcha_response = session.get("http://www.qingdaoport.net/adv/random.jsp")
        captcha = orc_response(captcha_response)

        print(captcha)

        response = session.post("http://www.qingdaoport.net/ywzx/ship/shipcx.jsp", data={
            'vessel_name': form.vessel.data,
            'voyage_number': form.voyage.data,
            'num': captcha})

        # html = etree.HTML(unicode.encode(response.text, encoding='utf-8'))
        html = etree.HTML(response.text)
        # print response.text

        session.close()

        columns = html.xpath('//table')[7][2].getchildren()

        if columns and len(columns) > 2:
            info = {
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
            }

            # encode_json = info['local']
            # json.dumps(info)


    return render_template('wharf.html', form=form, info=info)


@main.route('/yard', methods=['GET', 'POST'])
def yard():
    return render_template('yard.html')

@main.route('/express', methods=['GET', 'POST'])
def express():
    form = ExpressForm()
    infos = None
    if form.validate_on_submit():
        if form.express_number.data == '':
            infos = express_sources[form.express_name.data.encode("utf-8")].grab()
        else:
            infos = express_sources[form.express_name.data.encode("utf-8")].grab(form.express_number.data.encode("utf-8"))
    return render_template('express.html', form=form, infos=infos)
