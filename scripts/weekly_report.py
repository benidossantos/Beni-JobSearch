"""Gera o relatório de sexta-feira com os requisitos mais pedidos na semana.

Uso: python scripts/weekly_report.py 2026-10-16 relatorio.txt
Lê data/sent_jobs.json e considera as vagas enviadas de segunda até a data informada.
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Agrupa variações de escrita no mesmo requisito.
SINONIMOS = {
    "java": "Java", "spring": "Spring / Spring Boot", "spring boot": "Spring / Spring Boot",
    "python": "Python", "sql": "SQL", "mysql": "SQL", "javascript": "JavaScript",
    "typescript": "TypeScript", "react": "React", "angular": "Angular", "html": "HTML e CSS",
    "css": "HTML e CSS", "c#": "C# / .NET", ".net": "C# / .NET", "git": "Git",
    "api": "APIs REST", "apis": "APIs REST", "rest": "APIs REST", "power bi": "Power BI",
    "excel": "Excel / Google Sheets", "sheets": "Excel / Google Sheets", "testes": "Testes",
    "teste": "Testes", "qa": "Testes", "selenium": "Automação web (Selenium/Playwright)",
    "playwright": "Automação web (Selenium/Playwright)", "power automate": "Power Automate",
    "docker": "Docker", "kubernetes": "Kubernetes", "aws": "Cloud (AWS/Azure/GCP)",
    "azure": "Cloud (AWS/Azure/GCP)", "gcp": "Cloud (AWS/Azure/GCP)", "ingles": "Inglês",
    "agil": "Metodologias ágeis", "ageis": "Metodologias ágeis", "scrum": "Metodologias ágeis",
    "solid": "POO / SOLID", "poo": "POO / SOLID", "oop": "POO / SOLID",
    "graduacao": "Graduação (em andamento)", "logica": "Lógica de programação",
    "machine learning": "Machine Learning", "dados": "Manipulação de dados",
}


def normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def habilidades(requisito: str) -> set[str]:
    t = normalizar(requisito)
    achadas = {nome for chave, nome in SINONIMOS.items()
               if re.search(rf"(?<![a-z]){re.escape(chave)}(?![a-z])", t)}
    return achadas or {requisito.strip()}


def main(fim: str, saida: str) -> None:
    fim_d = date.fromisoformat(fim)
    inicio = fim_d - timedelta(days=fim_d.weekday())
    vagas = [v for v in json.loads((ROOT / "data/sent_jobs.json").read_text(encoding="utf-8"))
             if inicio <= date.fromisoformat(v["enviada_em"]) <= fim_d]
    total = Counter()
    por_area: dict[str, Counter] = {}
    for v in vagas:
        hs = set().union(*(habilidades(r) for r in v["requisitos"]))
        total.update(hs)
        area = v["area"].split(" /")[0].split(" (")[0]
        por_area.setdefault(area, Counter()).update(hs)

    n = len(vagas) or 1
    linhas = [
        "BENI JOBSEARCH - REQUISITOS MAIS PEDIDOS DA SEMANA",
        f"Período: {inicio:%d/%m} a {fim_d:%d/%m/%Y} · {len(vagas)} vagas analisadas",
        "",
        "TOP 10 GERAL",
    ]
    for i, (h, c) in enumerate(total.most_common(10), 1):
        linhas.append(f"{i:>2}. {h:<40} {c:>2} vagas ({c / n:.0%})")
    for area, cont in sorted(por_area.items()):
        linhas += ["", f"{area.upper()}"]
        linhas += [f"  - {h} ({c})" for h, c in cont.most_common(5)]
    Path(saida).write_text("\n".join(linhas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
