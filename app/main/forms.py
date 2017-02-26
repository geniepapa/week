# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

from .. import ship
from .. import wharf
from .. import express
from .. import yard


class WharfShipForm(FlaskForm):
    # port = SelectField(u"港口", choices=[(s, str.upper(s)) for s in wharf.sources])
    vessel = StringField(u"船名")
    voyage = StringField(u"航次")
    submit = SubmitField(u"查  询")


class WharfBillForm(FlaskForm):
    # port = SelectField(u"港口", choices=[(s, str.upper(s)) for s in wharf.sources])
    port_type = SelectField(u"进出口", choices=[('NONE', u"出口"),('JK', u"进口" )])
    bill_type = SelectField(u"提单类型", choices=[('ZTDH', u"主单"),('FTDH', u"分单" )])
    bill = StringField(u"提单号")
    submit = SubmitField(u"查  询")


class ShippingForm(FlaskForm):
    ship_name = SelectField(u"船公司", choices=[(s, str.upper(s)) for s in ship.sources])
    bill_number = StringField(u"提单号")
    submit = SubmitField(u"查  询")


class ExpressForm(FlaskForm):
    express_name = SelectField(u"快递公司", choices=[(s, str.upper(s)) for s in express.sources] )
    express_number = StringField(u"快递单号")
    submit = SubmitField(u"查  询")


class YardForm(FlaskForm):
    yard_name = SelectField(u"堆场", choices=[(s, s) for s in yard.sources])
    bill_number = StringField(u"提单号")
    submit = SubmitField(u"查  询")