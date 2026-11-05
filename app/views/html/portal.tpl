<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Portal · Estante</title><link rel="stylesheet" href="/static/css/style.css"></head>
<body><main class="login"><span class="tag">ESTANTE / BMVC</span><h1>Sua próxima leitura começa aqui.</h1><p>Entre no portal para consultar o catálogo de livros.</p>
% if error:
<p role="alert" class="error">{{error}}</p>
% end
<form action="/portal" method="post"><label for="username">Usuário</label><input id="username" name="username" autocomplete="username" required maxlength="200"><label for="password">Senha</label><input id="password" name="password" type="password" autocomplete="current-password" required><button>Entrar no catálogo →</button></form><small>Projeto de Programação Orientada a Objetos · Bottle MVC</small></main></body></html>
