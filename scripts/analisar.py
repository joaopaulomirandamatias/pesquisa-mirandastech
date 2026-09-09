#!/usr/bin/env python3
r"""Análise descritiva e comparação entre grupos a partir de um CSV — tabela em Markdown, teste com tamanho de efeito e IC, figura por script.

    python3 scripts/analisar.py dados.csv --variavel massa --grupo especie [--figura massa.png] [--markdown resultado.md]
    python3 scripts/analisar.py dados.csv --variavel massa --correlacao nadadeira
    python3 scripts/analisar.py dados.csv --categoria sexo --grupo especie          (tabela cruzada + qui-quadrado)

Regras: descritivas com n, média, DP, mediana, IQR e ausentes por grupo; 2 grupos → Welch t (com d de Cohen e IC 95 % da
diferença) e Mann-Whitney como robustez; 3+ grupos → ANOVA de Welch (η² aproximado) e Kruskal-Wallis; correlação → Pearson e
Spearman com IC; categoria × grupo → qui-quadrado e V de Cramér. Imprime tudo com 2 casas e o valor p exato (p < 0,001 quando
menor). A figura é gerada pelo script a partir dos dados (nunca desenhada à mão). Não decide nada: você interpreta.
"""
import argparse, math, sys
import numpy as np, pandas as pd
from scipy import stats

def fmt(p): return "p < 0,001" if p < 0.001 else f"p = {p:.3f}".replace(".", ",")
def br(x, d=2): return f"{x:.{d}f}".replace(".", ",")

def descritivas(df, v, g):
    linhas = ["| Grupo | n | Média | DP | Mediana | IQR | Ausentes |", "|---|---|---|---|---|---|---|"]
    grupos = [("todos", df)] + ([(k, s) for k, s in df.groupby(g)] if g else [])
    for k, s in grupos:
        x = s[v].dropna(); q1, q3 = x.quantile([0.25, 0.75]) if len(x) else (np.nan, np.nan)
        linhas.append(f"| {k} | {len(x)} | {br(x.mean())} | {br(x.std(ddof=1))} | {br(x.median())} | {br(q3 - q1)} | {s[v].isna().sum()} |")
    return "\n".join(linhas)

def comparar(df, v, g):
    grupos = {k: s[v].dropna().to_numpy() for k, s in df.groupby(g)}; grupos = {k: x for k, x in grupos.items() if len(x) >= 2}
    out = []
    if len(grupos) == 2:
        (ka, a), (kb, b) = grupos.items()
        t = stats.ttest_ind(a, b, equal_var=False); dif = a.mean() - b.mean()
        sp = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)); d = dif / sp
        se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)); ic = stats.t.ppf(0.975, t.df) * se
        u = stats.mannwhitneyu(a, b, alternative="two-sided")
        out.append(f"Teste t de Welch ({ka} − {kb}): diferença de médias = {br(dif)} (IC 95 % {br(dif - ic)} a {br(dif + ic)}), t({br(t.df, 1)}) = {br(t.statistic)}, {fmt(t.pvalue)}; d de Cohen = {br(d)}.")
        out.append(f"Mann-Whitney (robustez): U = {br(u.statistic, 0)}, {fmt(u.pvalue)}.")
    elif len(grupos) > 2:
        xs = list(grupos.values()); f = stats.f_oneway(*xs)
        todos = np.concatenate(xs); ssb = sum(len(x) * (x.mean() - todos.mean()) ** 2 for x in xs); sst = ((todos - todos.mean()) ** 2).sum(); eta = ssb / sst
        k = stats.kruskal(*xs)
        out.append(f"ANOVA de um fator entre {len(xs)} grupos: F({len(xs) - 1}, {len(todos) - len(xs)}) = {br(f.statistic)}, {fmt(f.pvalue)}; η² = {br(eta)}. Diferenças par a par pedem post hoc (ex.: Tukey ou Games-Howell) com correção.")
        out.append(f"Kruskal-Wallis (robustez): H = {br(k.statistic)}, {fmt(k.pvalue)}.")
    else: out.append("menos de dois grupos com n ≥ 2: nada a comparar.")
    return "\n".join(out)

def correlacao(df, v, w):
    s = df[[v, w]].dropna(); r = stats.pearsonr(s[v], s[w]); rho = stats.spearmanr(s[v], s[w]); ic = r.confidence_interval()
    return f"Pearson r = {br(r.statistic)} (IC 95 % {br(ic.low)} a {br(ic.high)}), n = {len(s)}, {fmt(r.pvalue)}; Spearman ρ = {br(rho.statistic)}, {fmt(rho.pvalue)}."

def cruzada(df, c, g):
    t = pd.crosstab(df[c], df[g]); chi = stats.chi2_contingency(t); n = t.to_numpy().sum(); v = math.sqrt(chi[0] / (n * (min(t.shape) - 1)))
    md = "| " + c + " \\ " + g + " | " + " | ".join(map(str, t.columns)) + " |\n|---|" + "---|" * len(t.columns) + "\n" + "\n".join("| " + str(i) + " | " + " | ".join(str(x) for x in r) + " |" for i, r in zip(t.index, t.to_numpy()))
    return md + f"\n\nQui-quadrado: χ²({chi[2]}) = {br(chi[0])}, {fmt(chi[1])}; V de Cramér = {br(v)}; n = {n}." + ("  Aviso: há células com esperado < 5 — considere o teste exato de Fisher." if (chi[3] < 5).any() else "")

def figura(df, v, g, caminho):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    if g:
        grupos = [(k, s[v].dropna()) for k, s in df.groupby(g)]
        ax.boxplot([x for _, x in grupos], tick_labels=[f"{k}\n(n={len(x)})" for k, x in grupos], showmeans=True)
        for i, (_, x) in enumerate(grupos, start=1): ax.scatter(np.random.default_rng(1).normal(i, 0.04, len(x)), x, s=8, alpha=0.35)
        ax.set_xlabel(g)
    else: ax.hist(df[v].dropna(), bins=20)
    ax.set_ylabel(v); ax.set_title(f"{v} por {g}" if g else v); fig.tight_layout(); fig.savefig(caminho); return caminho

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo"); ap.add_argument("--variavel"); ap.add_argument("--grupo"); ap.add_argument("--correlacao"); ap.add_argument("--categoria")
    ap.add_argument("--figura"); ap.add_argument("--markdown"); ap.add_argument("--sep", default=None)
    a = ap.parse_args(); df = pd.read_csv(a.arquivo, sep=a.sep, engine="python")
    partes = [f"# Análise de `{a.arquivo}` ({len(df)} linhas)"]
    if a.categoria and a.grupo: partes.append(cruzada(df, a.categoria, a.grupo))
    elif a.variavel:
        df[a.variavel] = pd.to_numeric(df[a.variavel], errors="coerce"); partes.append(descritivas(df, a.variavel, a.grupo))
        if a.grupo: partes.append(comparar(df, a.variavel, a.grupo))
        if a.correlacao: df[a.correlacao] = pd.to_numeric(df[a.correlacao], errors="coerce"); partes.append(correlacao(df, a.variavel, a.correlacao))
        if a.figura: partes.append(f"figura: {figura(df, a.variavel, a.grupo, a.figura)}")
    else: sys.exit("informe --variavel (com --grupo e/ou --correlacao) ou --categoria com --grupo")
    texto = "\n\n".join(partes); print(texto)
    if a.markdown: open(a.markdown, "w", encoding="utf-8").write(texto + "\n"); print(f"\ngravado: {a.markdown}")

if __name__ == "__main__": main()
