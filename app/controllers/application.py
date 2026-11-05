from dataclasses import asdict
from pathlib import Path

from bottle import HTTPError, request, response, redirect, template


class Application:
    def __init__(self, models):
        self.models = models
        self.views = Path(__file__).resolve().parents[1] / 'views' / 'html'
        self.pages = {'portal': self.portal, 'banco': self.banco}

    def render(self, page, **context):
        return self.pages[page](**context)

    def portal(self, error=None):
        return template('portal', template_lookup=[str(self.views)], error=error)

    def require_user(self, api=False):
        user = self.models.current_user(request.get_cookie('session_id'))
        if not user:
            if api:
                raise HTTPError(401, 'Autenticação necessária.')
            redirect('/portal', code=303)
        return user

    def login(self):
        token = self.models.authenticate(request.forms.getunicode('username', ''),
                                         request.forms.getunicode('password', ''))
        if not token:
            response.status = 401
            return self.portal(error='Usuário ou senha inválidos.')
        self.models.logout(request.get_cookie('session_id'))
        response.set_cookie('session_id', token, httponly=True, samesite='Strict',
                            secure=request.urlparts.scheme == 'https', path='/', max_age=3600)
        redirect('/banco', code=303)

    def logout(self):
        self.models.logout(request.get_cookie('session_id'))
        response.delete_cookie('session_id', path='/')
        redirect('/portal', code=303)

    def banco(self):
        user = self.require_user()
        response.set_header('Cache-Control', 'no-store')
        return template('banco', template_lookup=[str(self.views)], username=user, servicos=self.models.list_services())

    def write_service(self, service_id=None):
        self.require_user(api=True)
        if request.content_type.split(';')[0] == 'application/json':
            try:
                data = request.json
            except HTTPError:
                raise HTTPError(400, 'JSON inválido.')
        else:
            data = {key: request.forms.getunicode(key) for key in ('nome', 'tipo')}
        if not isinstance(data, dict):
            raise HTTPError(400, 'Envie nome e tipo.')
        values = [data.get(key) for key in ('nome', 'tipo')]
        if any(not isinstance(value, str) or not value.strip() or len(value.strip()) > 200 for value in values):
            raise HTTPError(400, 'Nome do serviço e tipo são obrigatórios e devem ter até 200 caracteres.')
        nome, tipo = (value.strip() for value in values)
        if service_id is None:
            service = self.models.create_service(nome, tipo)
            response.status = 201
            response.set_header('Location', '/banco')
            return asdict(service)
        if not self.models.update_service(service_id, nome, tipo):
            raise HTTPError(404, 'Serviço não encontrado.')
        return {'id': service_id, 'nome': nome, 'tipo': tipo}

    def delete_service(self, service_id):
        self.require_user(api=True)
        if not self.models.delete_service(service_id):
            raise HTTPError(404, 'Serviço não encontrado.')
        response.status = 204
        return ''
