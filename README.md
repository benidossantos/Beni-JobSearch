# Beni JobSearch

Automação que envia, **de segunda a sexta às 10h** (horário de Brasília), um e-mail para
`bernardo.claude.bot@gmail.com` com vagas júnior **100% remotas** em Desenvolvimento de Software,
Dados e IA, publicadas nos **últimos 7 dias**.

| Dia | O que chega no e-mail |
| --- | --- |
| Segunda a sexta | 10 vagas nacionais: 8 de pequenas e médias empresas (até ~500 funcionários) e 2 de grandes |
| Quinta-feira | + 5 vagas internacionais júnior abertas a candidatos no Brasil |
| Sexta-feira | + arquivo `.txt` com o resumo dos requisitos mais pedidos na semana |

Cada vaga mostra empresa, porte, área, há quantos dias foi publicada, fonte, requisitos,
salário (quando divulgado), avisos (vaga afirmativa, júnior/pleno, data não confirmada) e o link
para candidatura, de preferência o da página de carreiras da própria empresa.
O e-mail tem visual preto com letras brancas.

## Como funciona

A busca roda como uma **rotina agendada no Claude** (dispara às 9h45 para o e-mail chegar por volta das 10h):

1. Lê os critérios em `config.yaml` e o histórico em `data/sent_jobs.json`.
2. Busca vagas em Glassdoor, NerdIn, Remotar, ProgramaThor e páginas de carreira (Gupy, Lever,
   Greenhouse, Ashby); às quintas também em Himalayas, Remote Rocketship e We Work Remotely.
3. Filtra: júnior, 100% remoto, até 7 dias, área certa, ainda não enviada.
4. Gera o HTML com `scripts/render_email.py` e envia pelo Gmail.
5. Às sextas, gera o relatório com `scripts/weekly_report.py` e anexa ao e-mail.
6. Registra as vagas enviadas em `data/sent_jobs.json` e faz commit.

O passo a passo completo que a rotina segue está em [`ROUTINE.md`](ROUTINE.md).

## Resumo de requisitos (sextas-feiras)

Toda sexta o e-mail leva o arquivo `requisitos-mais-pedidos-AAAA-MM-DD.txt`, montado a partir de todas
as vagas enviadas de segunda a sexta. Ele traz:

- **Top 10 geral**: os requisitos que mais aparecem, com o número de vagas e a porcentagem;
- **Por área**: os 5 requisitos mais pedidos em Desenvolvimento, Dados e IA;
- **O que priorizar nos estudos**: de 4 a 6 recomendações curtas baseadas nos números da semana.

O script agrupa variações de escrita no mesmo requisito (por exemplo, "Spring" e "Spring Boot",
"MySQL" e "SQL", "C#" e ".NET") para a contagem não se dividir.
Um exemplo está em [`samples/relatorio-semanal-exemplo.txt`](samples/relatorio-semanal-exemplo.txt).

### Requisitos mais pedidos até agora

<!-- REQUISITOS:INICIO (atualizado automaticamente toda sexta-feira) -->
Base: 37 vagas enviadas de 13/10 a 16/10/2026 (inclui as 15 do e-mail de teste).

| # | Requisito | Vagas | % |
| --- | --- | --- | --- |
| 1 | APIs REST | 18 | 49% |
| 2 | SQL | 14 | 38% |
| 3 | Git | 14 | 38% |
| 4 | Java | 12 | 32% |
| 5 | JavaScript | 11 | 30% |
| 6 | TypeScript | 10 | 27% |
| 7 | Inglês | 10 | 27% |
| 8 | Testes | 9 | 24% |
| 9 | Spring / Spring Boot | 8 | 22% |
| 10 | React | 8 | 22% |

**O que priorizar:** APIs REST aparecem em quase metade das vagas, e SQL e Git em 4 de cada 10,
então valem para qualquer trilha. No back-end, Java + Spring Boot é a stack mais pedida; no front-end,
JavaScript/TypeScript com React. Inglês aparece em 1 de cada 4 vagas e em quase todas as internacionais,
e testes automatizados são um diferencial frequente.
<!-- REQUISITOS:FIM -->

## Arquivos

| Arquivo | Para quê |
| --- | --- |
| `config.yaml` | Destinatário, horário, dias de envio, cotas, fontes e regras de exclusão |
| `ROUTINE.md` | Passo a passo que a rotina agendada segue a cada execução |
| `templates/email.html.j2` | Modelo do e-mail (HTML com estilos inline, tema escuro) |
| `scripts/render_email.py` | Gera o HTML do e-mail a partir de um JSON de vagas |
| `scripts/weekly_report.py` | Gera o `.txt` de requisitos mais pedidos da semana |
| `data/sent_jobs.json` | Histórico das vagas enviadas (evita repetição e alimenta o relatório) |
| `samples/` | Exemplo de JSON do dia, e-mail renderizado e relatório semanal |

## Rodar localmente

```bash
pip install jinja2
python scripts/render_email.py samples/2026-10-13.json email.html
python scripts/weekly_report.py 2026-10-13 requisitos.txt
```

## Fontes que não dá para ler automaticamente

LinkedIn, Coodesh, Trampos, páginas de vaga da InHire e as listas de vagas no GitHub bloqueiam leitura
automática ou só carregam com JavaScript. Para incluir o LinkedIn sem violar os termos do site,
o caminho é criar alertas de vaga apontando para o e-mail do robô.
