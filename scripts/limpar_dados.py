#!/usr/bin/env python3
r"""Relatório de limpeza de uma tabela de dados (CSV ou XLSX) antes da análise — só leitura, com opção de gravar a versão limpa.

    python3 scripts/limpar_dados.py dados.csv [--sep ;] [--saida dados_limpos.csv]

Mostra: linhas e colunas; tipo inferido de cada coluna; valores ausentes por coluna (contagem e %); linhas duplicadas;
colunas de texto com espaços sobrando ou variantes de maiúsculas («Sim»/«sim »); colunas numéricas lidas como texto
(vírgula decimal, «NA», «-»); valores fora de faixa plausível (outliers pela regra 1,5 × IQR, só para conferir, não para apagar).
Com --saida grava a versão limpa: espaços aparados, ausentes padronizados, decimais com vírgula convertidos. Nunca apaga linhas:
a decisão sobre duplicatas e outliers é do pesquisador e vai para o diário da análise.
"""
import argparse, sys
import pandas as pd

AUSENTES = ["", "NA", "N/A", "na", "n/a", "-", "--", "?", "NaN", "nan", "null", "NULL", "None", "s/i", "S/I"]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo"); ap.add_argument("--sep", default=None, help="separador do CSV (padrão: detecta , ou ;)")
    ap.add_argument("--saida", default=None); ap.add_argument("--planilha", default=0, help="aba do XLSX (nome ou índice)")
    a = ap.parse_args()
    if a.arquivo.lower().endswith((".xlsx", ".xls", ".ods")):
        df = pd.read_excel(a.arquivo, sheet_name=a.planilha, dtype=str)
    else:
        df = pd.read_csv(a.arquivo, sep=a.sep, engine="python", dtype=str, keep_default_na=False)
    print(f"{a.arquivo}: {len(df)} linhas × {len(df.columns)} colunas\n")
    limpo = df.copy(); avisos = []
    for c in df.columns:
        s = df[c].astype(str)
        aparado = s.str.strip()
        if (aparado != s).sum(): avisos.append(f"{c}: {(aparado != s).sum()} valor(es) com espaço sobrando (aparado na saída)")
        aus = aparado.isin(AUSENTES); limpo[c] = aparado.mask(aus, pd.NA)
        num = pd.to_numeric(limpo[c].str.replace(".", "", regex=False).str.replace(",", ".", regex=False) if limpo[c].str.contains(",", na=False).any() and not limpo[c].str.contains(r"[A-Za-z]", na=False).any() else limpo[c], errors="coerce")
        n_ok = num.notna().sum(); n_val = limpo[c].notna().sum()
        if n_val and n_ok / n_val >= 0.9:
            tipo = "número"; limpo[c] = num
            if n_ok < n_val: avisos.append(f"{c}: {n_val - n_ok} valor(es) não numérico(s) numa coluna numérica → viraram ausentes; confira: {sorted(set(limpo[c][num.isna() & limpo[c].notna()].astype(str)))[:5]}")
            q1, q3 = num.quantile(0.25), num.quantile(0.75); iqr = q3 - q1
            out = num[(num < q1 - 1.5 * iqr) | (num > q3 + 1.5 * iqr)]
            if len(out): avisos.append(f"{c}: {len(out)} valor(es) fora de 1,5×IQR (mín {out.min():g}, máx {out.max():g}) — conferir na fonte, não apagar")
        else:
            tipo = "texto"
            vals = limpo[c].dropna().astype(str); low = vals.str.lower()
            if vals.nunique() != low.nunique(): avisos.append(f"{c}: variantes só por maiúsculas/minúsculas: {sorted(set(vals[low.duplicated(keep=False)]))[:6]}")
            if vals.nunique() <= 12: tipo = f"categórica ({vals.nunique()} valores: {', '.join(map(str, vals.value_counts().index[:6]))})"
        print(f"  {c:28} {tipo:50} ausentes: {int(aus.sum()):5} ({aus.mean()*100:4.1f}%)")
    dup = df.duplicated().sum()
    print(f"\nlinhas duplicadas (idênticas): {dup}")
    if avisos: print("\nAvisos:"); [print("  -", v) for v in avisos]
    if a.saida:
        limpo.to_csv(a.saida, index=False); print(f"\ngravado: {a.saida} ({len(limpo)} linhas; nenhuma linha removida)")

if __name__ == "__main__": main()
