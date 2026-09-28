# WoHelp: alterações em "Quem Somos" e "História"

São 3 pontos de edição, todos no mesmo template HTML. Nada mais muda.

---

## 1) CSS: colar imediatamente antes do `</style>` (depois do último `@media`)

Todas as classes são novas (`qs-` e `hist-`), então não afetam nenhuma outra aba.

```css
/* ===== Quem Somos e História (escopo restrito a essas duas abas) ===== */
.qs-cabecalho, .hist-cabecalho { max-width: 680px; margin: 0 auto 40px; }
.qs-cabecalho p, .hist-cabecalho p { margin: 14px 0 0; font-size: 16px; line-height: 1.8; }
.qs-linhas, .hist-linha, .qs-fontes { max-width: 820px; margin-left: auto; margin-right: auto; }

/* Quem Somos: linhas de definição separadas por filete */
.qs-linha { display: grid; grid-template-columns: minmax(150px, .34fr) minmax(0, 1fr); gap: 12px 40px; padding: 24px 0; border-top: 1px solid var(--line); }
.qs-linha h3 { margin: 0; font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 23px; line-height: 1.2; letter-spacing: -.4px; color: var(--plum); }
.qs-linha p { margin: 0; text-align: left; font-size: 15px; line-height: 1.8; }
.qs-ods { margin-top: 8px; padding: 26px 28px; border: 1px solid #e7dced; border-radius: 16px; background: linear-gradient(120deg, #f3eef7, #fbf3e4); }
.qs-ods h3 { margin: 0 0 10px; font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 23px; letter-spacing: -.4px; color: var(--plum); }
.qs-ods p { margin: 0 0 10px; text-align: left; font-size: 15px; line-height: 1.8; }
.qs-ods p:last-child { margin-bottom: 0; }

/* História: linha do tempo (a ordem aqui é realmente sequencial) */
.hist-linha { position: relative; padding-left: 38px; list-style: none; margin-top: 0; margin-bottom: 0; }
.hist-linha::before { content: ''; position: absolute; left: 8px; top: 8px; bottom: 8px; width: 2px; background: linear-gradient(var(--berry), var(--sand)); opacity: .4; }
.hist-item { position: relative; padding-bottom: 30px; }
.hist-item::before { content: ''; position: absolute; left: -38px; top: 4px; width: 18px; height: 18px; box-sizing: border-box; border-radius: 50%; background: #fff; border: 3px solid var(--berry); }
.hist-item.atual { padding-bottom: 0; }
.hist-item.atual::before { background: var(--sand); border-color: var(--sand); box-shadow: 0 0 0 6px rgba(228, 173, 85, .22); }
.hist-fase { font-size: 13px; font-weight: 800; color: var(--berry); }
.hist-item h3 { margin: 3px 0 8px; font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 24px; line-height: 1.2; letter-spacing: -.4px; color: var(--ink); }
.hist-item p { margin: 0; text-align: left; font-size: 15px; line-height: 1.8; max-width: 640px; }
.hist-dado { display: inline-block; margin-top: 12px; padding: 6px 12px; border: 1px solid #e4dbea; border-radius: 999px; background: #f7f3fa; color: #5b3974; font-size: 12px; font-weight: 800; }

.qs-fontes { margin-top: 34px; padding-top: 18px; border-top: 1px solid var(--line); font-size: 12px; line-height: 1.7; text-align: left; color: var(--ink-soft); }

@media (max-width: 700px) {
    .qs-linha { grid-template-columns: 1fr; gap: 8px; padding: 20px 0; }
    .qs-ods { padding: 22px 20px; }
    .hist-linha { padding-left: 32px; }
    .hist-item::before { left: -32px; }
    .hist-item h3 { font-size: 21px; }
}
```

---

## 2) HTML: substituir o bloco `<!-- ABA 2: QUEM SOMOS -->` inteiro

Do comentário até o `</div>` que fecha `id="quem-somos"`.

```html
        <!-- ABA 2: QUEM SOMOS -->
        <div id="quem-somos" class="aba-conteudo">
            <header class="qs-cabecalho">
                <span class="eyebrow">A rede</span>
                <h2>Uma rede de apoio para quem sonha com a ciência.</h2>
                <p>O WoHelp é uma plataforma que identifica as aspirações de estudantes do 2º ano do IFBA – Campus Simões Filho sobre as áreas em que pretendem trabalhar, com atenção especial às que querem seguir no campo científico. Ao reunir essas informações em um só lugar, ajuda a direcionar atividades formativas no campus de acordo com o que cada estudante pretende construir.</p>
            </header>

            <div class="qs-linhas">
                <div class="qs-linha">
                    <h3>O desafio</h3>
                    <p>As mulheres são maioria na educação formal, mas seguem menos presentes em áreas como computação e engenharia. Entre meninas de 15 anos da América Latina e do Caribe, cerca de 14% esperam trabalhar em uma ocupação STEM, contra cerca de 26% dos meninos (PISA 2022, OCDE). A diferença já aparece antes da escolha de uma graduação.</p>
                </div>
                <div class="qs-linha">
                    <h3>Nossa proposta</h3>
                    <p>Registrar as aspirações das estudantes e transformá-las em um diagnóstico. Com ele, o IFBA – Simões Filho pode planejar atividades formativas alinhadas às pretensões acadêmicas de quem quer entrar na ciência.</p>
                </div>
                <div class="qs-linha">
                    <h3>Quem apoiamos</h3>
                    <p>Estudantes do 2º ano do IFBA – Campus Simões Filho, um campus com cursos exclusivamente do segmento industrial. Pesquisa com egressos do IFBA mostra que, nos eixos de Controle e Processos Industriais e de Produção Industrial, as matrículas femininas e masculinas em Simões Filho são mais equilibradas que no campus Salvador (Costa, 2025).</p>
                </div>
            </div>

            <section class="qs-ods qs-linhas" aria-labelledby="qs-ods-titulo">
                <h3 id="qs-ods-titulo">Tecnologia a serviço da igualdade</h3>
                <p>O WoHelp está alinhado ao ODS 5. Atende à meta 5.b, que trata do uso de tecnologias de informação e comunicação para o empoderamento das mulheres, e à meta 5.5, com foco na dimensão assistiva de garantir a participação plena das mulheres em espaços de decisão, incluindo o campo científico.</p>
                <p>Esse segundo ponto importa: nas Bolsas de Produtividade em Pesquisa do CNPq, as mulheres ocupavam 35,6% de 12.917 bolsas analisadas e estavam sub-representadas em posições deliberativas da política científica (Saúde em Debate, 2021).</p>
                <p>O projeto participa da Semana Nacional de Ciência e Tecnologia 2026, cujo tema é Ciência Delas.</p>
            </section>

            <p class="qs-fontes">Fontes: OCDE, relatório sobre diferenças de gênero em educação, habilidades e carreiras STEM na América Latina e no Caribe (2025); COSTA, Fabiana Freitas. Juventude e Educação Profissional de Nível Médio – percursos generificados? 22º Congresso Brasileiro de Sociologia, 2025; Saúde em Debate (2021), sobre as Bolsas PQ/CNPq.</p>
        </div>
```

---

## 3) HTML: substituir o bloco `<!-- ABA 3: HISTÓRIA -->` inteiro

Do comentário até o `</div>` que fecha `id="historia"`.

```html
        <!-- ABA 3: HISTÓRIA -->
        <div id="historia" class="aba-conteudo">
            <header class="hist-cabecalho">
                <span class="eyebrow">O caminho até aqui</span>
                <h2>Nossa História</h2>
                <p>O WoHelp se apoia em uma constatação das pesquisas: a desigualdade de gênero na ciência não começa na universidade nem no mercado de trabalho. Ela se forma ao longo de toda a trajetória. Esta é a linha do tempo que motiva o projeto.</p>
            </header>

            <ol class="hist-linha">
                <li class="hist-item">
                    <span class="hist-fase">Infância</span>
                    <h3>Estereótipos desde cedo</h3>
                    <p>Antes de escolher uma faculdade, crianças já recebem mensagens sobre o que combina com meninos e com meninas. A OCDE (2022) indica que pais, professores, escola e colegas influenciam como esses estereótipos são internalizados, mesmo quando ninguém os diz de forma direta.</p>
                </li>
                <li class="hist-item">
                    <span class="hist-fase">Escolha da área</span>
                    <h3>Menos meninas em STEM</h3>
                    <p>Na América Latina e no Caribe, as mulheres são cerca de 40% dos formados em STEM, mas a participação cai em áreas específicas. No Brasil, apenas cerca de 15% dos graduados em TIC são mulheres.</p>
                    <span class="hist-dado">Aos 15 anos: 14% das meninas e 26% dos meninos esperam uma carreira STEM</span>
                </li>
                <li class="hist-item">
                    <span class="hist-fase">Referências</span>
                    <h3>Poucos modelos femininos</h3>
                    <p>Com poucas mulheres visíveis nessas áreas, faltam exemplos reais de trajetória. OCDE e UNESCO apontam modelos femininos e mentoria como estratégias eficazes. Em estudo nos Estados Unidos, ter professoras de STEM aumentou em 14% as chances de as alunas seguirem STEM, e em 44% as das mulheres de alto desempenho.</p>
                </li>
                <li class="hist-item">
                    <span class="hist-fase">Primeiras oportunidades</span>
                    <h3>O que a pesquisa mostrou no IFBA</h3>
                    <p>Em pesquisa com egressos do IFBA dos campi Salvador e Simões Filho, as mulheres eram maioria (56%), mas apareceram menos entre quem fez estágio remunerado em empresas, experiência vista pelos estudantes como ampliadora da empregabilidade.</p>
                    <span class="hist-dado">Atuaram na área do curso: 23,84% das mulheres e 46,02% dos homens</span>
                </li>
                <li class="hist-item">
                    <span class="hist-fase">Carreira científica</span>
                    <h3>Progressão e liderança</h3>
                    <p>Um estudo de 2020 com docentes da pós-graduação brasileira não encontrou diferença de produção científica entre homens e mulheres, mas identificou diferenças favoráveis aos homens no recebimento de bolsas de produtividade. Entre as bolsas PQ/CNPq analisadas, 35,6% eram de mulheres.</p>
                </li>
                <li class="hist-item">
                    <span class="hist-fase">Mercado de trabalho</span>
                    <h3>Diferenças de rendimento</h3>
                    <p>Em 2024, entre os profissionais das ciências e intelectuais, o rendimento médio das mulheres foi de R$ 5.378, contra R$ 8.291 dos homens (IBGE), cerca de 64,9% do masculino. É uma diferença média, que também reflete a distribuição desigual entre profissões.</p>
                </li>
                <li class="hist-item atual">
                    <span class="hist-fase">Hoje</span>
                    <h3>O WoHelp</h3>
                    <p>O projeto reúne essas evidências em uma proposta concreta: identificar as aspirações de estudantes do 2º ano do IFBA – Campus Simões Filho, com foco nas que pretendem entrar no campo científico, e concentrar esses dados em uma única plataforma para orientar atividades formativas no campus. Alinhado ao ODS 5 (metas 5.b e 5.5), o WoHelp participa da Semana Nacional de Ciência e Tecnologia 2026, com o tema Ciência Delas.</p>
                    <span class="tag-em-breve">Em construção 🌱</span>
                </li>
            </ol>

            <p class="qs-fontes">Fontes: OCDE (2022; 2025); UNESCO; IBGE (2024); Saúde em Debate (2021); COSTA, Fabiana Freitas. Juventude e Educação Profissional de Nível Médio – percursos generificados? 22º Congresso Brasileiro de Sociologia, 2025.</p>
        </div>
```
