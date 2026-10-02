# Alterações no templates/index.html (5 trechos; o resto do arquivo fica intacto)

## 1. NAV — remover o botão "Pesquisa"
Apagar as 2 linhas:
    <!-- BOTÃO NOVO DA PESQUISA -->
    <button ... id="btn-pesquisa" ...>Pesquisa</button>

## 2. CADASTRO — trocar TODO o `<form action="/cadastrar" ...> ... </form>` por:
```html
<form action="/cadastrar" method="POST" class="login-form" id="form-cadastro">
  <div id="cad-etapa-1" class="cad-etapa">
    <span class="cad-passo">Etapa 1 de 2 · Seus dados</span>
    <div class="campo"><label for="nome">Como podemos te chamar?</label>
      <input type="text" id="nome" name="nome" placeholder="Como podemos te chamar?" autocomplete="name" maxlength="120" required></div>
    <div class="campo"><label for="idade">Sua idade</label>
      <input type="number" id="idade" name="idade" placeholder="Qual é a sua idade?" min="1" max="120" inputmode="numeric" required></div>
    <div class="campo"><label for="curso">Curso</label>
      <input type="text" id="curso" name="curso" placeholder="Qual é o seu curso?" maxlength="120" required></div>
    <div class="campo"><label for="turma">Turma</label>
      <input type="text" id="turma" name="turma" placeholder="Qual é a sua turma?" maxlength="60" required></div>
    <button type="button" class="btn-principal" onclick="avancarCadastro()">Continuar
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></button>
  </div>
  <div id="cad-etapa-2" class="cad-etapa" hidden>
    <span class="cad-passo">Etapa 2 de 2 · Seus interesses e experiências</span>
    <div class="campo"><label>1. Você entrou no curso com interesse em seguir na área técnica?</label>
      <div class="cad-radios" data-motivo="m-motivo_desinteresse" data-mostrar="Não">
        <label><input type="radio" name="interesse_area_tecnica" value="Sim" required> Sim</label>
        <label><input type="radio" name="interesse_area_tecnica" value="Não"> Não</label></div>
      <div class="cad-motivo" id="m-motivo_desinteresse" hidden><label for="motivo_desinteresse">Por quê?</label>
        <input type="text" id="motivo_desinteresse" name="motivo_desinteresse" maxlength="300" placeholder="Nos conte o motivo"></div></div>
    <div class="campo"><label>2. Você deseja continuar os estudos depois de concluir o ensino médio integrado?</label>
      <div class="cad-radios" data-motivo="m-motivo_continuar_estudos" data-mostrar="Não">
        <label><input type="radio" name="continuar_estudos" value="Sim" required> Sim</label>
        <label><input type="radio" name="continuar_estudos" value="Não"> Não</label></div>
      <div class="cad-motivo" id="m-motivo_continuar_estudos" hidden><label for="motivo_continuar_estudos">Por quê?</label>
        <input type="text" id="motivo_continuar_estudos" name="motivo_continuar_estudos" maxlength="300" placeholder="Nos conte o motivo"></div></div>
    <div class="campo"><label>3. Você sofreu algum tipo de violência no curso, por ser menina, que te desmotivou para seguir na área técnica?</label>
      <div class="cad-radios" data-motivo="m-motivo_violencia_curso" data-mostrar="Sim">
        <label><input type="radio" name="violencia_curso" value="Sim" required> Sim</label>
        <label><input type="radio" name="violencia_curso" value="Não"> Não</label></div>
      <div class="cad-motivo" id="m-motivo_violencia_curso" hidden><label for="motivo_violencia_curso">Por quê?</label>
        <input type="text" id="motivo_violencia_curso" name="motivo_violencia_curso" maxlength="300" placeholder="Se quiser, conte o que aconteceu"></div></div>
    <div class="campo"><label>4. Você imagina sofrer algum tipo de violência em curso depois do integrado, na área técnica, que te desmotive, enquanto mulher, a cursar um curso nessas áreas?</label>
      <div class="cad-radios" data-motivo="m-motivo_violencia_futura" data-mostrar="Sim">
        <label><input type="radio" name="violencia_futura" value="Sim" required> Sim</label>
        <label><input type="radio" name="violencia_futura" value="Não"> Não</label></div>
      <div class="cad-motivo" id="m-motivo_violencia_futura" hidden><label for="motivo_violencia_futura">Por quê?</label>
        <input type="text" id="motivo_violencia_futura" name="motivo_violencia_futura" maxlength="300" placeholder="Se quiser, conte o que imagina"></div></div>
    <div class="cad-acoes">
      <button type="button" class="btn-principal cad-voltar" onclick="voltarCadastro()">Voltar</button>
      <button type="submit" class="btn-principal">Finalizar cadastro</button></div>
  </div>
</form>
```
Observação: o texto do botão antigo era "Iniciar Jornada"; trocado por "Continuar"/"Finalizar cadastro" conforme o fluxo pedido.

## 3. PERFIL — no input `perfil-aspiracao`, remover o atributo `required`
(aspiração e universidade deixaram de fazer parte do cadastro; ficam opcionais no perfil.)

## 4. PESQUISA — apagar o bloco inteiro `<!-- ABA: PESQUISA (DUAS ETAPAS) --> <div id="pesquisa"...> ... </div>`
No `<script>`:
- apagar `avancarPesquisa()` e `voltarPesquisa()`;
- substituir `toggleMotivo` e o handler de `load` por:
```js
function avancarCadastro() {
  const e1 = document.getElementById('cad-etapa-1');
  const campos = e1.querySelectorAll('input');
  for (const c of campos) { if (!c.reportValidity()) return; }
  e1.hidden = true; document.getElementById('cad-etapa-2').hidden = false;
}
function voltarCadastro() {
  document.getElementById('cad-etapa-2').hidden = true; document.getElementById('cad-etapa-1').hidden = false;
}
function toggleMotivo(radios, valor) {
  const box = document.getElementById(radios.dataset.motivo), inp = box.querySelector('input');
  const mostrar = valor === radios.dataset.mostrar; box.hidden = !mostrar; if (!mostrar) inp.value = '';
}
document.addEventListener('change', (e) => {
  const r = e.target.closest && e.target.closest('.cad-radios');
  if (r && e.target.type === 'radio') toggleMotivo(r, e.target.value);
});
window.addEventListener('load', () => {
  const b = document.querySelector('.btn-nav.ativo'); if (b) moverIndicador(b);
});
```

## 5. CSS — acrescentar ao final do `<style>`
```css
.cad-etapa { display: grid; grid-template-columns: 1fr; gap: 14px; grid-column: span 2; }
.cad-etapa[hidden], .cad-motivo[hidden] { display: none; }
.cad-motivo { margin-top: 10px; }
.login-form .cad-etapa .campo:last-of-type { grid-column: auto; }
.cad-passo { font-size: 11px; font-weight: 800; letter-spacing: 1.4px; text-transform: uppercase; color: var(--berry); }
.cad-radios { display: flex; gap: 18px; margin: 4px 0 10px; }
.cad-radios label { display: flex; align-items: center; gap: 6px; margin: 0; font-size: 14px; font-weight: 600; }
.cad-radios input { width: auto; min-height: 0; }
.cad-acoes { display: flex; gap: 12px; }
.cad-acoes .btn-principal { margin-top: 7px; width: auto; flex: 1; }
.cad-acoes .btn-principal:last-child { flex: 2; }
.cad-voltar { background: #eef1f6; color: #342450; box-shadow: none; }
```

## 6. CSS extra (já incluído pelo script)
```css
.login-form .cad-etapa .btn-principal { grid-column: auto; }
```
