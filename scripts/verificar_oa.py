#!/usr/bin/env python3
"""Para cada DOI de um CSV (coluna doi), consulta o Unpaywall e acrescenta is_oa, oa_status e pdf_url.
    python3 verificar_oa.py entrada.csv saida.csv --email seu@email.br
Só biblioteca padrão; uma chamada por DOI; limite do serviço: 100.000 chamadas/dia."""
import argparse, csv, json, time, urllib.parse, urllib.request
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("entrada"); ap.add_argument("saida"); ap.add_argument("--email", required=True); ap.add_argument("--max", type=int, default=100000); a = ap.parse_args()
    rows = list(csv.DictReader(open(a.entrada, encoding="utf-8"))); n_oa = 0
    for i, r in enumerate(rows[: a.max]):
        doi = (r.get("doi") or "").replace("https://doi.org/", "").strip(); r.update({"is_oa": "", "oa_status": "", "pdf_url": ""})
        if not doi: continue
        try:
            with urllib.request.urlopen(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={a.email}", timeout=30) as resp: d = json.load(resp)
            best = d.get("best_oa_location") or {}; r.update({"is_oa": d.get("is_oa"), "oa_status": d.get("oa_status"), "pdf_url": best.get("url_for_pdf") or best.get("url") or ""}); n_oa += bool(d.get("is_oa"))
        except Exception as e: r["oa_status"] = f"erro: {str(e)[:40]}"
        time.sleep(0.1)
    with open(a.saida, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} registros · {n_oa} com versão aberta · gravado {a.saida}")
if __name__ == "__main__": main()
