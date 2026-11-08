"""阶段 1 baseline: 字符 n-gram TF-IDF + 逻辑回归。
输出 AUC、Precision@K、高区分度词榜，以及留一类目的跨类目测试。
用法: python3 src/baseline.py data/notes_labeled.csv
"""
import sys
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

df = pd.read_csv(sys.argv[1])
df["text"] = df["title"].fillna("") + " " + df["tags"].fillna("")


def fit(train, test):
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3), min_df=2)
    Xtr = vec.fit_transform(train["text"])
    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(Xtr, train["label_viral"])
    p = clf.predict_proba(vec.transform(test["text"]))[:, 1]
    return vec, clf, p


def precision_at_k(y, p, frac=0.1):
    k = max(1, int(len(y) * frac))
    idx = np.argsort(-p)[:k]
    return float(np.asarray(y)[idx].mean())


train, test = train_test_split(df, test_size=0.25, stratify=df["label_viral"], random_state=0)
vec, clf, p = fit(train, test)
print("== 同分布测试 ==")
print("AUC:", round(roc_auc_score(test["label_viral"], p), 3))
print("Precision@10%:", round(precision_at_k(test["label_viral"], p), 3),
      "(基准爆款率:", round(test["label_viral"].mean(), 3), ")")

names = np.array(vec.get_feature_names_out())
order = np.argsort(-clf.coef_[0])
top = pd.DataFrame({"term": names[order][:30], "coef": clf.coef_[0][order][:30].round(3)})
top.to_csv("outputs/top_terms.csv", index=False, encoding="utf-8-sig")
print("\n== 最能区分爆款的字串（前 15）==")
print(top.head(15).to_string(index=False))

print("\n== 留一类目（用其余类目训练）==")
for c in df["category"].unique():
    tr, te = df[df["category"] != c], df[df["category"] == c]
    _, _, pc = fit(tr, te)
    print(f"{c}: AUC={roc_auc_score(te['label_viral'], pc):.3f}  P@10%={precision_at_k(te['label_viral'], pc):.3f}")
