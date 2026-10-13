# Beni JobSearch

Envia todo dia às 10h (horário de Brasília) um e-mail com 10 vagas júnior 100% remotas
em Desenvolvimento de Software, Dados e IA, publicadas nos últimos 7 dias:
8 de pequenas e médias empresas e 2 de grandes. Às quintas-feiras o mesmo e-mail traz
também 5 vagas internacionais júnior abertas a candidatos no Brasil.

A busca roda como uma rotina agendada no Claude. Este repositório guarda:

| Arquivo | Para quê |
| --- | --- |
| `config.yaml` | Critérios de busca, cotas, fontes e regras de exclusão |
| `templates/email.html.j2` | Modelo do e-mail (HTML com estilos inline) |
| `scripts/render_email.py` | Gera o HTML a partir de um JSON de vagas |
| `data/sent_jobs.json` | Histórico das vagas já enviadas, para não repetir |
| `samples/` | E-mails de exemplo |

Gerar um e-mail localmente:

```bash
pip install jinja2
python scripts/render_email.py samples/2026-10-13.json saida.html
```
