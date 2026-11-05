<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Banco · JAM-DF</title><link rel="stylesheet" href="/static/css/style.css"></head>
<body><main><header><span class="tag">JAM-DF / SEGURANÇA ELETRÔNICA</span><form action="/logout" method="post"><span>{{username}}</span> <button class="secondary">Sair</button></form></header><p class="eyebrow">SEGURANÇA ELETRÔNICA EM UM SÓ LUGAR</p><h1>Serviços JAM-DF</h1><p>Consulte os serviços de instalação, manutenção e consultoria de segurança.</p><section class="panel"><div class="section-title"><h2>Serviços cadastrados</h2><span>{{len(servicos)}} cadastrado(s)</span></div>
% if servicos:
<div class="table-wrap"><table><thead><tr><th>ID</th><th>Serviço</th><th>Tipo</th></tr></thead><tbody>
% for servico in servicos:
<tr><td>#{{servico.id}}</td><td>{{servico.nome}}</td><td>{{servico.tipo}}</td></tr>
% end
</tbody></table></div>
% else:
<div class="empty"><h3>Nenhum serviço cadastrado.</h3><p>Cadastre o primeiro serviço pelo terminal usando os exemplos do README.</p></div>
% end
</section><aside><strong>Gerenciamento pelo terminal</strong><p>A criação, edição e exclusão são realizadas por cURL autenticado. Consulte o README para os comandos.</p></aside></main></body></html>
