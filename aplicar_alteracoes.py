"""Uso: python aplicar_alteracoes.py templates/index.html
Gera templates/index.novo.html (o original NÃO é modificado). Falha se algum trecho não for encontrado."""
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]); md = pathlib.Path(__file__).with_name("index_html_alteracoes.md").read_text(encoding="utf-8")
blocks = re.findall(r"```(\w+)\n(.*?)```", md, re.S)
form, js, css = (next(b for l, b in blocks if l == k) for k in ("html", "js", "css"))
css_extra = "\n".join(b for l, b in blocks if l == "css")
html = src.read_text(encoding="utf-8")

def sub(pat, rep, label, flags=re.S):
    global html
    html, n = re.subn(pat, lambda m: rep, html, count=1, flags=flags)
    if n != 1: sys.exit(f"ERRO: trecho não encontrado -> {label}")

sub(r'[ \t]*<!-- BOTÃO NOVO DA PESQUISA -->\s*<button[^>]*id="btn-pesquisa"[^>]*>Pesquisa</button>\s*\n', "", "botão Pesquisa")
sub(r'<form action="/cadastrar".*?</form>', form.strip(), "form de cadastro")
html, n = re.subn(r'(<input[^>]*id="perfil-aspiracao"[^>]*?)\s+required', r'\1', html, count=1, flags=re.S)
if n != 1: sys.exit("ERRO: input perfil-aspiracao")
sub(r'<!-- ABA: PESQUISA \(DUAS ETAPAS\) -->.*?(?=<!-- Script para as abas -->)', "", "aba Pesquisa")
sub(r"window\.addEventListener\('load'.*?\n            \}\);", "", "handler load")
sub(r"// Lógica interna da nova pesquisa.*?(?=window\.addEventListener\('resize')", js.strip() + "\n\n            ", "funções da pesquisa")
sub(r"</style>", css_extra + "\n    </style>", "fechamento do style", flags=0)
out = src.with_name("index.novo.html"); out.write_text(html, encoding="utf-8"); print("OK ->", out)
