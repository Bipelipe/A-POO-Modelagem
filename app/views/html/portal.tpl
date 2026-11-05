<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Portal · JAM-DF</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body class="portal-page">
  <main class="login-layout">
    <section class="brand-panel" aria-labelledby="brand-title">
      <a class="brand" href="/portal">JAM-DF</a>
      <div class="brand-message">
        <p class="eyebrow">SEGURANÇA ELETRÔNICA</p>
        <h1 id="brand-title">Proteção em cada detalhe.</h1>
        <p>Organização e confiança para cuidar do que importa.</p>
        <ul class="specialties"><li>Instalação</li><li>Manutenção</li><li>Consultoria</li></ul>
      </div>
      <small>JAM-DF · Portal de serviços</small>
    </section>
    <section class="login-panel" aria-labelledby="login-title">
      <div class="login-card">
        <p class="eyebrow">ÁREA DO CLIENTE</p>
        <h2 id="login-title">Bem-vindo de volta</h2>
        <p>Identifique-se para consultar nossos serviços.</p>
% if error:
        <p role="alert" class="error">{{error}}</p>
% end
        <form action="/portal" method="post">
          <label for="username">Usuário</label>
          <input id="username" name="username" autocomplete="username" placeholder="Seu usuário" required maxlength="200">
          <label for="password">Senha</label>
          <input id="password" name="password" type="password" autocomplete="current-password" placeholder="Sua senha" required>
          <button class="login-button" type="submit">Acessar portal <span aria-hidden="true">→</span></button>
        </form>
        <p class="login-footnote">Acesso exclusivo para usuários cadastrados.</p>
      </div>
    </section>
  </main>
</body>
</html>
