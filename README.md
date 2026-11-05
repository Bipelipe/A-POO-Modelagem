# Estante — catálogo de livros com BMVC

Sistema do nível 2 de Programação Orientada a Objetos, baseado em
[hgmachine/bmvc_start_from_this](https://github.com/hgmachine/bmvc_start_from_this).
Mantém a arquitetura Bottle MVC da referência: rotas em `route.py`, controlador
`Application`, persistência em `DataRecord`, modelos em `app/models`, templates
em `app/views/html` e estilos em `app/static`.

## Executar no Linux

Requer Python 3.10 ou superior, com suporte a venv, e cURL para as operações de escrita.

```bash
cd /workspace/A-POO-Modelagem # ou o diretório do seu clone
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python route.py
```

Abra `http://localhost:8080/portal`. Na primeira execução é criada uma conta de
demonstração: usuário **admin**, senha **admin123**. O login leva a `/banco`, que
mostra os livros com ID, título e autor. Uma lista vazia é esperada inicialmente.
O botão Sair encerra a sessão. O banco exige autenticação em todas as operações.

Para definir outra conta inicial, configure `BMVC_USERNAME` e `BMVC_PASSWORD`
antes da primeira execução. Essas variáveis não alteram contas já persistidas.
Não use a senha de demonstração em uma implantação pública. As senhas são
armazenadas com salt aleatório e PBKDF2-SHA256, nunca em texto puro.

O SQLite é criado em `app/controllers/db/catalogo.sqlite3` (ignorado no Git).
`BMVC_DB` permite escolher outro arquivo; `HOST` e `PORT` alteram a interface e
porta. Os livros e usuários sobrevivem ao reinício; as sessões duram uma hora e
ficam em memória, exigindo novo login após reiniciar o servidor. Cookies usam
HttpOnly e SameSite=Strict, e Secure quando a requisição chega por HTTPS.
O servidor embutido é destinado a desenvolvimento local.

## CRUD por cURL

Com o servidor rodando, execute em outro terminal Linux. Use o mesmo arquivo de
cookies nos comandos; ele contém sua sessão e não deve ser versionado.

```bash
BASE=http://localhost:8080
COOKIE=$(mktemp)

# Login: resposta 303 e cookie de sessão
curl -i -c "$COOKIE" -d 'username=admin&password=admin123' "$BASE/portal"

# CREATE: resposta 201 com o ID gerado
curl -i -b "$COOKIE" -H 'Content-Type: application/json' \
  -d '{"titulo":"Dom Casmurro","autor":"Machado de Assis"}' "$BASE/banco"

# READ: abra /banco no navegador após fazer login no portal.
# Pelo terminal também é possível consultar o HTML:
curl -b "$COOKIE" "$BASE/banco"

# Substitua 1 pelo ID retornado no CREATE.
# UPDATE: resposta 200
curl -i -b "$COOKIE" -X PUT -H 'Content-Type: application/json' \
  -d '{"titulo":"Memórias Póstumas de Brás Cubas","autor":"Machado de Assis"}' \
  "$BASE/banco/1"

# DELETE: resposta 204, sem corpo
curl -i -b "$COOKIE" -X DELETE "$BASE/banco/1"

# Logout: resposta 303
curl -i -b "$COOKIE" -X POST "$BASE/logout"
rm "$COOKIE"
```

Atualize a página `/banco` após cada operação para observar o resultado.
POST e PUT também aceitam formulário (`--data-urlencode 'titulo=...'` e
`--data-urlencode 'autor=...'`). Campos vazios ou com mais de 200 caracteres
retornam 400; IDs inexistentes retornam 404; escritas sem sessão retornam 401.

## Validação

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Os testes usam SQLite temporário e exercitam login, bloqueio de acesso, logout,
CRUD, validação de dados, escape de HTML e persistência após recriar a aplicação.

## Texto explicativo para a entrega

O projeto Estante oferece os recursos portal e banco seguindo a estrutura BMVC.
O portal autentica contas representadas pelo modelo User_account e gera uma
sessão individual por cliente. Apenas clientes autenticados acessam o banco,
que apresenta a lista de objetos Livro, com os atributos título e autor.
O READ é implementado na página banco; CREATE, UPDATE e DELETE são executados
por requisições cURL no terminal Linux. O controlador Application coordena as
requisições e utiliza DataRecord para persistir os modelos em SQLite. As views
TPL apresentam o formulário de login e a listagem de livros.

Para entregar, envie os arquivos ao seu repositório GitHub e inclua o link junto
com o texto acima. Não inclua `.venv`, banco local ou cookies no commit.
