from flask import request
from app.utils.response_formatter import make_response

def auth_middleware(app):
    @app.before_request
    def auth():
        EXCLUDED_ROUTES = ['/api/docs/']

        if any(request.path.startswith(prefix) for prefix in EXCLUDED_ROUTES):
            return None

        token = request.headers.get('Authorization')
        
        if not token:
            return make_response(message="Token não encontrado", status="error", code=401)