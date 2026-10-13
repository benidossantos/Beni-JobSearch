"""Renderiza o e-mail diário a partir de um JSON de vagas.

Uso: python scripts/render_email.py samples/2026-10-13.json saida.html
"""
import json
import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]
DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
        "sexta-feira", "sábado", "domingo"]


def data_extenso(d: date) -> str:
    return f"{DIAS[d.weekday()]}, {d.day} de {MESES[d.month - 1]} de {d.year}"


def main(entrada: str, saida: str) -> None:
    dados = json.loads(Path(entrada).read_text(encoding="utf-8"))
    for v in dados["vagas"]:
        v["grupo"] = "grande" if v["porte"].startswith("grande") else "pme"
    env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                      autoescape=select_autoescape(["html", "j2"]))
    html = env.get_template("email.html.j2").render(
        data_extenso=data_extenso(date.fromisoformat(dados["data"])),
        vagas=dados["vagas"],
        internacionais=dados.get("internacionais", []),
        observacoes=dados.get("observacoes", []),
    )
    Path(saida).write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
