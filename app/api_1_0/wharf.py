from flask import jsonify, request
from . import api, auth
from ..wharf import sources as wharf_sources


@api.route('/wharf/<string:name>', methods=['POST'])
@auth.login_required
def get_wharf(name):
    return jsonify(wharf_sources[unicode.encode(name)].grab(request.json['vessel'], request.json['voyage']))
