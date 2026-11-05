<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Banco · Estante</title><link rel="stylesheet" href="/static/css/style.css"></head>
<body><main><header><span class="tag">ESTANTE / BMVC</span><form action="/logout" method="post"><span>{{username}}</span> <button class="secondary">Sair</button></form></header><p class="eyebrow">SEU ACERVO EM UM SÓ LUGAR</p><h1>Catálogo de livros</h1><p>Explore as histórias cadastradas no banco.</p><section class="panel"><div class="section-title"><h2>Todos os livros</h2><span>{{len(livros)}} cadastrado(s)</span></div>
% if livros:
<div class="table-wrap"><table><thead><tr><th>ID</th><th>Título</th><th>Autor</th></tr></thead><tbody>
% for livro in livros:
<tr><td>#{{livro.id}}</td><td>{{livro.titulo}}</td><td>{{livro.autor}}</td></tr>
% end
</tbody></table></div>
% else:
<div class="empty"><h3>Sua estante ainda está vazia.</h3><p>Cadastre o primeiro livro pelo terminal usando os exemplos do README.</p></div>
% end
</section><aside><strong>Gerenciamento pelo terminal</strong><p>A criação, edição e exclusão são realizadas por cURL autenticado. Consulte o README para os comandos.</p></aside></main></body></html>
