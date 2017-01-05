# coding: utf-8

import requests
from flask import render_template
from lxml import etree

from ..ship import sources as ship_sources
from forms import WharfForm, ShippingForm, ExpressForm
from . import main
from ..express import sources as express_sources
from ..util.ocr import orc_response
from ..wharf import sources as wharf_sources


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
        if form.vessel.data == '':
            info = wharf_sources[form.port.data.encode("utf-8")] .grab()
        else:
            info = wharf_sources[form.port.data.encode("utf-8")]\
                .grab(form.vessel.data.encode("utf-8"), form.voyage.data.encode("utf-8"))

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
