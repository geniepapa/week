from flask import jsonify, request
from . import api, auth
from ..wharf import sources as wharf_sources


@api.route('/wharf/<string:name>/ship', methods=['POST'])
@auth.login_required
def get_wharf_ship(name):
    return jsonify(wharf_sources[unicode.encode(name)].grab(request.json['vessel'], request.json['voyage']))


@api.route('/wharf/<string:name>/bill', methods=['POST'])
@auth.login_required
def get_wharf_bill(name):
    return jsonify(wharf_sources[unicode.encode(name)].grab_trade(request.json['bill']))
