from flask import jsonify
from app.yard import sources as yard_sources
from . import api, auth


@api.route('/yard/<string:company>/<string:numb>')
@auth.login_required
def get_yard(company, numb):
    return jsonify(yard_sources[unicode.encode(company)].grab(unicode.encode(numb)))
