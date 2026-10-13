# Rotina diária do Beni JobSearch

Instruções que a rotina agendada segue a cada execução (segunda a sexta, por volta das 10h de Brasília).
Os critérios e as fontes estão em `config.yaml`; este arquivo diz **como** executar.

## 1. Preparar
1. Ler `config.yaml` e `data/sent_jobs.json`.
2. Ver o dia da semana em America/Sao_Paulo:
   - quinta-feira → também buscar 5 vagas internacionais;
   - sexta-feira → também gerar o relatório de requisitos (.txt).
   - sábado ou domingo → não enviar nada e encerrar.

## 2. Buscar vagas nacionais (limite: ~15 consultas)
Na ordem, até ter candidatas suficientes:
1. `https://www.glassdoor.com.br/Vaga/trabalho-remoto-<termo>-vagas-SRCH_IL.0,15_IS12226_KO16,<fim>.htm?fromAge=7`
   com termos: `desenvolvedor-jr`, `dados-junior`, `python-junior`, `programador-junior`.
   O Glassdoor mostra a idade da vaga; abrir a vaga só para ler requisitos.
2. NerdIn: `https://www.nerdin.com.br/vagas.php?pagina=1..3` — filtrar Junior + Home Office.
3. Remotar: `https://api.remotar.com.br/jobs?search=desenvolvedor%20j%C3%BAnior` e `...search=dados%20j%C3%BAnior`
   — traz `createdAt` e o link da página de carreiras da empresa (preferir esse link).
4. ProgramaThor: `https://programathor.com.br/jobs` — marca porte "Pequena/média empresa".
5. Indeed só como último recurso (sem data → "data não confirmada").

Filtros obrigatórios (descartar se falhar):
- júnior/jr/trainee; nada pleno/sênior; nada que exija mais de 2 anos;
- 100% remoto (ler a descrição: títulos com "híbrido" ou endereço presencial saem);
- publicada há no máximo 7 dias;
- área: Desenvolvimento de Software, QA, Dados, BI, IA/ML;
- não está em `data/sent_jobs.json` (comparar link e empresa+título);
- não é exclusiva para PcD (afirmativa não exclusiva entra com aviso).

Seleção: 8 de pequenas/médias (até ~500 funcionários) + 2 grandes.
Se faltarem pequenas/médias, completar com vagas de data não confirmada, sinalizadas.
Se mesmo assim faltar, enviar menos de 10 e explicar numa observação no topo.

## 3. Quinta-feira: 5 vagas internacionais
Fontes: `https://himalayas.app/jobs/countries/brazil/junior-developer`,
`https://www.remoterocketship.com/country/latin-america/jobs/junior-software-engineer/`,
`https://weworkremotely.com/categories/remote-programming-jobs.rss`.
Regras: empresa sediada fora do Brasil, aceita candidatos no Brasil, júnior (ou júnior/pleno com aviso),
publicada há no máximo 7 dias. Usar o link original de candidatura (Ashby, Lever, Greenhouse, Workable).

## 4. Montar e enviar
1. Gravar o JSON do dia em `samples/AAAA-MM-DD.json` no mesmo formato de `samples/2026-10-13.json`
   (campos: titulo, empresa, porte, area, publicada, requisitos[3-5], link, fonte; opcionais salario, aviso).
2. `pip install jinja2` (se preciso) e `python scripts/render_email.py samples/AAAA-MM-DD.json /tmp/email.html`.
3. Sexta-feira: atualizar o histórico primeiro (passo 5), depois
   `python scripts/weekly_report.py AAAA-MM-DD /tmp/requisitos.txt` e acrescentar no fim a seção
   "O QUE PRIORIZAR NOS ESTUDOS" (4 a 6 itens curtos, baseados nos números).
4. Enviar pelo conector Gmail (`send_message`) para `bernardo.claude.bot@gmail.com`:
   - assunto: `Beni JobSearch · N vagas júnior remotas · DD/MM` (quinta: acrescentar `+ 5 internacionais`;
     sexta: acrescentar `+ relatório de requisitos`);
   - `htmlBody` = conteúdo de /tmp/email.html; `body` = resumo em texto puro;
   - sexta: anexar /tmp/requisitos.txt em base64, `mimeType: text/plain`,
     nome `requisitos-mais-pedidos-AAAA-MM-DD.txt`.

## 5. Registrar
Acrescentar cada vaga enviada a `data/sent_jobs.json`
(`empresa, titulo, area, porte, requisitos, link, enviada_em`), fazer commit
`Envio de DD/MM: N vagas` e `git push origin main`.

## 6. Sexta-feira: atualizar o README
Substituir o trecho entre `<!-- REQUISITOS:INICIO` e `<!-- REQUISITOS:FIM -->` no `README.md` pelo
resultado acumulado de todas as vagas em `data/sent_jobs.json` (base, tabela top 10 e um parágrafo
"O que priorizar"). Incluir no mesmo commit do envio.

## Economia
- No máximo ~15 consultas web por dia (~22 às quintas).
- Não reler páginas já lidas; abrir a página da vaga só quando a listagem não traz requisitos.
- Nunca escrever o HTML à mão: sempre usar `scripts/render_email.py`.
