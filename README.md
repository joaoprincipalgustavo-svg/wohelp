# WoHelp

Aplicação Flask em português para cadastro e edição de perfis. A interface HTML existente continua disponível e o backend também oferece endpoints HTTP/JSON. O backend permanece em Python. A persistência usa SQLite localmente e PostgreSQL quando `DATABASE_URL` aponta para PostgreSQL.

## Executar localmente

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export WOHELP_SECRET_KEY="uma-chave-local-longa"
python app.py
```

Abra <http://127.0.0.1:5000>. Sem `DATABASE_URL`, o app continua usando `wohelp.db` na raiz, o arquivo legado que acompanha o projeto. Esse arquivo não é apagado ou alterado por uma migração. Para rodar os testes: `python -m unittest discover -s tests`.

## API

Os objetos de resposta de perfil têm `id`, `nome`, `idade`, `aspiracao` e `universidade`. A API usa a sessão Flask em cookie; clientes que chamam de outra origem devem enviar credenciais (`credentials: "include"`) e a origem precisa estar em `CORS_ORIGINS`.

| Método e rota | Uso |
| --- | --- |
| `GET /health` | Verifica a disponibilidade do app e banco |
| `POST /api/alunos` | Cria cadastro JSON; retorna `201` e define a sessão |
| `GET /api/perfil` | Lê o perfil da sessão atual |
| `PATCH /api/perfil` | Atualiza o perfil da sessão; envia os quatro campos |

Exemplo:

```json
{"nome":"Ana Silva","idade":20,"aspiracao":"Ser médica","universidade":"UFBA"}
```

Erros de validação retornam `400` com `{ "error": "..." }`; a leitura/edição sem uma sessão válida retorna `401`. Idade aceita inteiros de 1 a 120, e os campos de texto têm limites de tamanho. Os formulários HTML antigos (`/cadastrar`, `/perfil/atualizar`) seguem disponíveis.

## Configuração

- `DATABASE_URL`: URL SQLAlchemy do banco. Ausente, usa o SQLite incluído. Para PostgreSQL use a connection string do provedor escolhido, como Neon.
- `WOHELP_SECRET_KEY`: chave longa e aleatória para assinar cookies de sessão; obrigatória em produção.
- `CORS_ORIGINS`: origens permitidas, separadas por vírgula, sem barra final, por exemplo `https://meu-frontend.onrender.com`. Deixe vazio se frontend e backend forem servidos pela mesma origem.
- `SESSION_COOKIE_SECURE`: use `true` em HTTPS. `render.yaml` define esse valor.
- `SESSION_COOKIE_SAMESITE`: padrão `Lax`. Para frontend em domínio diferente que dependa de cookies, defina `None` e use HTTPS (`SESSION_COOKIE_SECURE=true`).
- A sessão do perfil dura 30 dias e é renovada enquanto a pessoa usa o site. Assim, fechar e reabrir o navegador não exige preencher o cadastro de novo; mantenha `WOHELP_SECRET_KEY` estável entre reinicializações.
- `FLASK_DEBUG`: só para desenvolvimento local; padrão desativado.

Não inclua segredos em arquivos versionados. Os campos obrigatórios do perfil são nome, idade e aspiração; universidade é opcional.

## Deploy no Render

1. Envie este projeto para um repositório Git e conecte-o ao Render.
2. Crie um banco PostgreSQL em um provedor com plano gratuito, por exemplo [Neon](https://neon.com/pricing), e copie a connection string. A URL contém credenciais: mantenha-a privada.
3. Crie os recursos a partir de `render.yaml` (Blueprint). Ele configura um serviço web Python no plano gratuito, comando Gunicorn ligado à porta fornecida pelo Render, health check e geração de `WOHELP_SECRET_KEY`. Quando o Render solicitar `DATABASE_URL`, cole a URL do PostgreSQL.
4. Configure `CORS_ORIGINS` no serviço web se o frontend for hospedado em outra origem. Neste projeto frontend e backend são servidos juntos, então pode ficar vazio.
5. Faça o deploy e confira `/health`.

O PostgreSQL gratuito do Render expira após 30 dias e pode ser excluído depois do período de recuperação; por isso o Blueprint não cria esse banco. O plano gratuito do serviço web do Render pode dormir depois de 15 minutos sem tráfego, e a primeira abertura após isso pode demorar cerca de um minuto. O banco Neon gratuito tem limites de uso e pode pausar quando ocioso. Confira os limites atuais e mantenha exportações de segurança dos dados; um plano gratuito não é garantia de backup ou disponibilidade. Consulte as [limitações dos planos gratuitos do Render](https://render.com/docs/free), a [página de planos Neon](https://neon.com/pricing) e o [formato de Blueprint](https://render.com/docs/blueprint-spec). O Render fornece HTTPS e o cookie de sessão é marcado como seguro.

### PostgreSQL e migração dos dados SQLite existentes

O app cria a tabela `alunos` se ainda não existir. Isso não transfere os dados do arquivo local. Faça backup do arquivo `wohelp.db` antes de qualquer operação. Para levar os registros existentes ao PostgreSQL:

1. Crie o banco PostgreSQL (por exemplo, no plano gratuito do Neon) e copie a connection string.
2. Em uma máquina que tenha o arquivo original e conectividade ao banco, instale `requirements.txt` e defina `DATABASE_URL` com essa URL.
3. Execute `python migrate_sqlite_to_postgres.py`. Opcionalmente escolha outro arquivo fonte com `SQLITE_SOURCE=/caminho/wohelp.db`.
4. O comando copia IDs e registros sem alterar a origem, recusa destino que já contenha registros e compara a contagem e a lista de IDs ao final. Em seguida faça o deploy usando esse mesmo banco.

Não rode o comando de migração sobre banco de produção que já recebeu cadastros: ele recusa tabela não vazia. Mantenha a cópia SQLite original como backup até verificar a implantação e os dados.

### Teste de cadastros reais

Após deploy, use o link público do serviço para validar a tela, criar um cadastro e editar o perfil. Os registros ficam no PostgreSQL configurado. Restrinja o acesso ao banco e não compartilhe sua connection string.
