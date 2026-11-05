<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Portal · JAM-DF</title><link rel="stylesheet" href="/static/css/style.css"></head>
<body><main class="login"><span class="tag">JAM-DF / SEGURANÇA ELETRÔNICA</span><h1>Segurança com organização e confiança.</h1><p>Entre no portal JAM-DF para consultar os serviços de segurança eletrônica.</p>
% if error:
<p role="alert" class="error">{{error}}</p>
% end
<form action="/portal" method="post"><label for="username">Usuário</label><input id="username" name="username" autocomplete="username" required maxlength="200"><label for="password">Senha</label><input id="password" name="password" type="password" autocomplete="current-password" required><button>Entrar no catálogo →</button></form><small>Projeto de Programação Orientada a Objetos · Bottle MVC</small></main></body></html>
