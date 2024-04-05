from flask import Blueprint, request, jsonify, g
from application.use_cases import CreateUser
from infrastructure.adapters.user_repository_adapter_sqlalchemy import UserRepositorySQLAlchemy
from sqlalchemy.orm import scoped_session

bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@bp.route('/', methods=['POST'])
def create_user():
    user_data = request.get_json()

    user_repository = UserRepositorySQLAlchemy(g.session)
    user_case = CreateUser(user_repository)

    created_user = user_case.execute(user_data)

    return jsonify(created_user), 201