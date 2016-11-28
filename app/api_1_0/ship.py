from flask import jsonify

from app.ship import sources as ship_sources
from . import api, auth


@api.route('/ship/<string:company>/<string:numb>')
@auth.login_required
def get_ship(company, numb):
    return jsonify(ship_sources[unicode.encode(company)].grab(unicode.encode(numb)))

