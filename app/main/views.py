# coding: utf-8

from flask import render_template
from . import main
from forms import WharfBillForm, WharfShipForm, ShippingForm, ExpressForm, YardForm
from ..ship import sources as ship_sources
from ..express import sources as express_sources
from ..wharf import sources as wharf_sources
from ..yard import sources as yard_sources


@main.route('/', methods=['GET', 'POST'])
def index():
    return shipping()


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


@main.route('/wharf/ship', methods=['GET', 'POST'])
def wharf_ship():
    form = WharfShipForm()
    info = None
    if form.validate_on_submit():
        if form.vessel.data == '':
            # info = wharf_sources[form.port.data.encode("utf-8")] .grab_ship()
            info = wharf_sources['qingdao'].grab_ship()
        else:
            # info = wharf_sources[form.port.data.encode("utf-8")]\
            #    .grab_ship(form.vessel.data.encode("utf-8"), form.voyage.data.encode("utf-8"))
            info = wharf_sources['qingdao'] \
                .grab_ship(form.vessel.data.encode("utf-8"), form.voyage.data.encode("utf-8"))

    return render_template('wharf_ship.html', form=form, info=info)


@main.route('/wharf/bill', methods=['GET', 'POST'])
def wharf_bill():
    form = WharfBillForm()
    info = None
    if form.validate_on_submit():
        if form.bill.data == '':
            # info = wharf_sources[form.port.data.encode("utf-8")] .grab_bill()
            info = wharf_sources['qingdao'].grab_bill()
        else:
            # info = wharf_sources[form.port.data.encode("utf-8")]\
            #    .grab_bill(form.bill.data.encode("utf-8"), form.port_type.data.encode("utf-8"))
            info = wharf_sources['qingdao'].grab_bill(form.port_type.data.encode("utf-8"),
                                                      form.bill_type.data.encode("utf-8"),
                                                      form.bill.data.encode("utf-8"))

    return render_template('wharf_bill.html', form=form, info=info)


@main.route('/yard', methods=['GET', 'POST'])
def yard():
    form = YardForm()
    info = None
    if form.validate_on_submit():
        if form.bill_number.data == '':
            info = yard_sources[form.yard_name.data].grab()
        else:
            info = yard_sources[form.yard_name.data].grab(form.bill_number.data.encode("utf-8"))

    return render_template('yard.html', form=form, info=info)


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


