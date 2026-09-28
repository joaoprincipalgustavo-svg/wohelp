#!/usr/bin/env python3
"""Atualiza SOMENTE as abas "Quem Somos" e "História" do template do WoHelp.
Uso: python aplicar_quem_somos_historia.py templates/index.html
Cria um backup .bak e falha (sem alterar nada) se algum ponto de ancoragem não for encontrado."""
import re, sys, shutil

CSS = """
        /* ===== Quem Somos e História (estilos escopados: .qs-* e .hist-*) ===== */
        .qs-wrap, .hist-wrap { max-width: 980px; margin: 0 auto; }
        .qs-lead { max-width: 660px; margin: 14px auto 36px; font-size: 16px; line-height: 1.8; }
        .qs-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
        .qs-card { padding: 26px 26px 24px; border: 1px solid var(--line); border-radius: 16px; background: #fbfbfd; }
        .qs-card h3, .hist-item h3 { margin: 0 0 8px; font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 22px; line-height: 1.2; letter-spacing: -.3px; color: var(--plum); }
        .qs-card p, .hist-item p { margin: 0; text-align: left; font-size: 14.5px; line-height: 1.75; }
        .qs-card p + p, .hist-item p + p { margin-top: 10px; }
        .qs-tag { display: block; margin-bottom: 10px; font-size: 11px; font-weight: 800; letter-spacing: 1.4px; text-transform: uppercase; color: var(--berry); }
        .qs-dados { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 16px; }
        .qs-dado { padding: 22px 20px; border: 1px solid #e7dced; border-radius: 16px; background: linear-gradient(145deg, #f3eef7, #faf6ec); }
        .qs-dado strong { display: block; font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 32px; line-height: 1; letter-spacing: -.5px; color: var(--plum); }
        .qs-dado span { display: block; margin-top: 10px; font-size: 12.5px; line-height: 1.55; color: var(--ink-soft); }
        .qs-fonte { max-width: 760px; margin: 14px auto 0; font-size: 11.5px; line-height: 1.6; color: #8a8493; }
        .hist-lead { max-width: 640px; margin: 14px auto 0; font-size: 16px; line-height: 1.8; }
        .hist-linha { position: relative; max-width: 760px; margin: 40px auto 0; padding-left: 34px; }
        .hist-linha::before { content: ''; position: absolute; left: 7px; top: 8px; bottom: 30px; width: 2px; background: linear-gradient(var(--berry), var(--sand)); opacity: .35; }
        .hist-item { position: relative; padding-bottom: 32px; }
        .hist-item::before { content: ''; position: absolute; left: -34px; top: 4px; width: 16px; height: 16px; box-sizing: border-box; border: 3px solid var(--berry); border-radius: 50%; background: #fff; }
        .hist-item.atual::before { border-color: var(--sand); background: var(--sand); }
        .hist-etapa { display: block; margin-bottom: 6px; font-size: 11px; font-weight: 800; letter-spacing: 1.4px; text-transform: uppercase; color: var(--berry); }
        .hist-nota { margin-top: 4px; text-align: center; }
        @media (max-width: 640px) {
            .qs-grid, .qs-dados { grid-template-columns: 1fr; }
            .qs-card { padding: 22px 20px; }
            .hist-linha { padding-left: 28px; }
            .hist-item::before { left: -28px; }
        }
"""

QUEM_SOMOS = """<!-- ABA 2: QUEM SOMOS -->
        <div id="quem-somos" class="aba-conteudo">
            <div class="qs-wrap">
                <span class="eyebrow">Quem somos</span>
                <h2>Ouvir o que elas sonham para abrir caminhos na ciência.</h2>
                <p class="qs-lead">O WoHelp é uma plataforma que identifica as aspirações de estudantes do 2º ano do IFBA – Campus Simões Filho sobre as áreas em que pretendem atuar, com atenção especial às que têm como perspectiva entrar no campo científico.</p>

                <div class="qs-grid">
                    <article class="qs-card">
                        <span class="qs-tag">Nossa proposta</span>
                        <h3>Reunir dados para orientar a formação</h3>
                        <p>O projeto reúne, em uma única plataforma, informações sobre as pretensões acadêmicas das estudantes. Com esse retrato, é possível direcionar atividades formativas e afins no IFBA – Simões Filho de acordo com o que elas querem seguir.</p>
                        <p>O cadastro é o primeiro passo: nele, a estudante conta como quer ser chamada, onde pretende estudar e qual é a sua maior aspiração hoje.</p>
                    </article>
                    <article class="qs-card">
                        <span class="qs-tag">O problema</span>
                        <h3>Um desafio que começa cedo</h3>
                        <p>Estereótipos de gênero atravessam a infância e a escola e moldam o que meninas imaginam para o futuro, antes mesmo da escolha de uma graduação. Depois, as mulheres seguem menos representadas em áreas STEM e em posições de prestígio e decisão na ciência.</p>
                    </article>
                    <article class="qs-card">
                        <span class="qs-tag">Quem queremos apoiar</span>
                        <h3>Estudantes do 2º ano em Simões Filho</h3>
                        <p>Nosso foco são as estudantes que pensam em seguir no campo científico. O campus tem oferta exclusiva de cursos industriais e, segundo pesquisa com egressos do IFBA, as mulheres são minoria entre quem conseguiu estágio remunerado em empresas.</p>
                    </article>
                    <article class="qs-card">
                        <span class="qs-tag">Tecnologia e STEM</span>
                        <h3>Tecnologia a serviço da igualdade</h3>
                        <p>O WoHelp está alinhado ao ODS 5. Atende à meta 5.b, que trata do uso de tecnologias de informação e comunicação para o empoderamento das mulheres, e à meta 5.5, com foco na dimensão assistiva de garantir a participação plena das mulheres em espaços de decisão, incluindo o campo científico.</p>
                        <p>O projeto participa da Semana Nacional de Ciência e Tecnologia 2026, com o tema Ciência Delas.</p>
                    </article>
                </div>

                <div class="qs-dados">
                    <div class="qs-dado"><strong>14% vs. 26%</strong><span>das meninas e dos meninos de 15 anos, respectivamente, esperavam trabalhar em ocupações STEM (PISA 2022, América Latina e Caribe).</span></div>
                    <div class="qs-dado"><strong>23,84% vs. 46,02%</strong><span>das mulheres e dos homens egressos do ensino técnico industrial do IFBA já haviam atuado na área do curso.</span></div>
                    <div class="qs-dado"><strong>35,6%</strong><span>das bolsas de produtividade em pesquisa do CNPq analisadas em estudo de 2021 eram de mulheres.</span></div>
                </div>
                <p class="qs-fonte">Fontes: OCDE (2022; 2025); Costa (2025), 22º Congresso Brasileiro de Sociologia; estudo publicado na revista Saúde em Debate (2021).</p>
            </div>
        </div>"""

HISTORIA = """<!-- ABA 3: HISTÓRIA -->
        <div id="historia" class="aba-conteudo">
            <div class="hist-wrap">
                <span class="eyebrow">O caminho até aqui</span>
                <h2>Nossa História</h2>
                <p class="hist-lead">O WoHelp se apoia em uma cadeia de desigualdades que as pesquisas descrevem ao longo da trajetória das mulheres na ciência. Entender essa cadeia ajuda a explicar por que o projeto começa pelas estudantes do 2º ano.</p>

                <div class="hist-linha">
                    <div class="hist-item">
                        <span class="hist-etapa">Etapa 1 · Na infância</span>
                        <h3>Estereótipos desde cedo</h3>
                        <p>A OCDE afirma que crianças e jovens são afetados por estereótipos de gênero desde idades precoces, e que pais, professores, escola e colegas influenciam como essas ideias são internalizadas. Mesmo sem serem ditas diretamente, expectativas e incentivos diferentes podem moldar os interesses das estudantes.</p>
                    </div>
                    <div class="hist-item">
                        <span class="hist-etapa">Etapa 2 · Na escolha da área</span>
                        <h3>Menos mulheres em STEM</h3>
                        <p>Na América Latina e no Caribe, as mulheres são cerca de 40% dos formados em cursos STEM, mas, no Brasil, apenas cerca de 15% dos graduados em TIC. Com poucas mulheres nessas áreas, faltam referências: OCDE e UNESCO apontam modelos femininos e programas de mentoria como estratégias eficazes contra vieses de gênero.</p>
                    </div>
                    <div class="hist-item">
                        <span class="hist-etapa">Etapa 3 · Na formação técnica</span>
                        <h3>O caminho no IFBA</h3>
                        <p>Pesquisa com egressos de dois campi do IFBA, Salvador e Simões Filho, mostra que as mulheres eram maioria entre as 338 participantes do questionário, mas minoria entre quem realizou estágio remunerado em empresas. Entre quem chegou ao último ano do curso, 23,84% das mulheres já haviam atuado na área, contra 46,02% dos homens. As trajetórias podem começar com oportunidades diferentes.</p>
                    </div>
                    <div class="hist-item">
                        <span class="hist-etapa">Etapa 4 · Na carreira científica</span>
                        <h3>Progressão e reconhecimento</h3>
                        <p>Um estudo com docentes da pós-graduação brasileira (2013 a 2016) não encontrou diferença de produção científica entre homens e mulheres, mas identificou diferenças favoráveis aos homens nas bolsas de produtividade em pesquisa. Em 2024, segundo o IBGE, entre os profissionais das ciências e intelectuais, o rendimento médio das mulheres correspondia a cerca de 64,9% do dos homens. É uma diferença média, que não prova sozinha discriminação salarial direta.</p>
                    </div>
                    <div class="hist-item atual">
                        <span class="hist-etapa">Etapa 5 · Agora</span>
                        <h3>O WoHelp</h3>
                        <p>É nesse ponto que o WoHelp entra. A plataforma começa pelas estudantes do 2º ano do IFBA – Campus Simões Filho, identificando as áreas em que querem atuar e reunindo esses dados para orientar atividades formativas na instituição.</p>
                        <p>Hoje, a plataforma já permite o cadastro e a atualização do perfil, e o chat de apoio segue em construção. O projeto participa da Semana Nacional de Ciência e Tecnologia 2026, com o tema Ciência Delas.</p>
                    </div>
                </div>
                <p class="hist-nota"><span class="tag-em-breve">O registro detalhado das etapas do projeto será acrescentado aqui 🌱</span></p>
            </div>
        </div>"""

def main(path):
    src = open(path, encoding="utf-8").read()
    if src.count("</style>") != 1:
        sys.exit("Âncora </style> não encontrada exatamente uma vez. Nada foi alterado.")
    out = src.replace("</style>", CSS + "    </style>", 1)
    for ini, fim, novo in (("<!-- ABA 2: QUEM SOMOS -->", "<!-- ABA 3: HISTÓRIA -->", QUEM_SOMOS),
                           ("<!-- ABA 3: HISTÓRIA -->", "<!-- ABA 4: CHAT -->", HISTORIA)):
        padrao = re.compile(re.escape(ini) + r".*?(?=\s*" + re.escape(fim) + ")", re.S)
        if len(padrao.findall(out)) != 1:
            sys.exit(f"Bloco '{ini}' não encontrado. Nada foi alterado.")
        out = padrao.sub(lambda _: novo, out, count=1)
    shutil.copy(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(out)
    print("OK: abas Quem Somos e História atualizadas. Backup em", path + ".bak")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "templates/index.html")
