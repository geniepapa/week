from flask import jsonify, g
from . import auth, api
from ..models import User


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True


@api.route('/token')
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


