"""按类目内分位数生成爆款标签。
用法: python3 src/make_labels.py data/notes.csv data/notes_labeled.csv [--normalize] [--q 0.8]
--normalize: 用 互动数/(粉丝数+100) 代替互动数，削弱粉丝量的影响。
"""
import argparse
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--normalize", action="store_true")
ap.add_argument("--q", type=float, default=0.8)
a = ap.parse_args()

df = pd.read_csv(a.src)
df["engagement"] = df["likes"] + df["collects"] + df["comments"]
score = df["engagement"] / (df["author_followers"] + 100) if a.normalize else df["engagement"]
df["score"] = score
thr = df.groupby("category")["score"].transform(lambda s: s.quantile(a.q))
df["label_viral"] = (df["score"] >= thr).astype(int)
df["title_len"] = df["title"].str.len()
df.to_csv(a.dst, index=False, encoding="utf-8-sig")
print(df.groupby("category")["label_viral"].agg(["count", "mean"]).round(3))
