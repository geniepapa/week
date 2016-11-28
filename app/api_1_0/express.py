from flask import jsonify
from . import api, auth
from ..express import sources as express_sources


@api.route('/express/<string:company>/<string:numb>')
@auth.login_required
def get_express(company, numb):
    return jsonify(express_sources[unicode.encode(company)].grab(unicode.encode(numb)))
