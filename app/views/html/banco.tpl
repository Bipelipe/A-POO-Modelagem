<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Serviços · JAM-DF</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body class="dashboard-page">
  <aside class="sidebar">
    <a class="brand" href="/banco"><span class="brand-mark" aria-hidden="true">J</span> JAM-DF</a>
    <p class="sidebar-caption">PORTAL DO CLIENTE</p>
    <nav aria-label="Menu principal"><a class="nav-active" href="/banco" aria-current="page"><span aria-hidden="true">▦</span> Serviços</a></nav>
    <div class="sidebar-bottom"><span class="status-dot" aria-hidden="true"></span> Segurança eletrônica</div>
  </aside>
  <div class="dashboard-content">
    <header class="topbar">
      <span>Portal <span class="breadcrumb-separator">/</span> <strong>Serviços</strong></span>
      <form action="/logout" method="post"><span class="user-name">{{username}}</span><button class="secondary" type="submit">Sair</button></form>
    </header>
    <main class="workspace">
      <section class="page-heading">
        <div><p class="eyebrow">JAM-DF / CATÁLOGO</p><h1>Nossos serviços</h1><p>Soluções para a segurança da sua casa e da sua empresa.</p></div>
        <div class="counter"><strong>{{len(servicos)}}</strong><span>serviço(s) cadastrado(s)</span></div>
      </section>
      <section class="panel" aria-labelledby="services-title">
        <div class="section-title"><div><h2 id="services-title">Catálogo de serviços</h2><p>Instalação, manutenção e consultoria de segurança.</p></div><span class="label-chip">JAM-DF</span></div>
% if servicos:
        <div class="table-wrap"><table><thead><tr><th scope="col">Código</th><th scope="col">Serviço</th><th scope="col">Tipo</th></tr></thead><tbody>
% for servico in servicos:
          <tr><td class="service-code">#{{servico.id}}</td><td class="service-name">{{servico.nome}}</td><td><span class="type-badge">{{servico.tipo}}</span></td></tr>
% end
        </tbody></table></div>
% else:
        <div class="empty"><span class="empty-symbol" aria-hidden="true">▦</span><h3>Nenhum serviço cadastrado</h3><p>Os serviços cadastrados aparecerão aqui.</p></div>
% end
        <footer class="panel-footer">{{len(servicos)}} registro(s) no catálogo</footer>
      </section>
      <footer class="workspace-footer"><span>JAM-DF</span><span>Segurança com organização e confiança.</span></footer>
    </main>
  </div>
</body>
</html>
