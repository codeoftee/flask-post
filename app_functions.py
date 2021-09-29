from flask import session, request

from models import User


def check_login():
    """this function will return user object
        from database or None if user does not
        exist
    """
    if 'email' in session:
        # user has active session
        user = User.query.filter(User.email == session['email']).first()
        return user
    else:
        username = request.cookies.get('username')
        user = User.query.filter_by(username=username).first()
        return user
