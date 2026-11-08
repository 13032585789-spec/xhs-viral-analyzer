"""生成合成演示数据，只用来跑通流程。真实数据请替换 data/notes.csv。"""
import csv, math, random

random.seed(0)
CATS = {
    "美妆": ["粉底液", "口红", "防晒", "眼影", "底妆", "卸妆"],
    "穿搭": ["大衣", "牛仔裤", "通勤", "小个子", "针织衫", "乐福鞋"],
    "学习": ["考研", "雅思", "背单词", "笔记", "时间管理", "考试周"],
}
VIRAL = ["干货", "亲测", "避雷", "平价", "一定要", "保姆级", "我悔了"]
NEUTRAL = ["分享", "日常", "记录", "今天", "最近", "关于", "体验"]

rows = []
for i in range(600):
    cat = random.choice(list(CATS))
    kw = random.choice(CATS[cat])
    n_v = random.choice([0, 0, 0, 1, 1, 2])
    words = random.sample(VIRAL, n_v) + random.sample(NEUTRAL, random.choice([1, 2]))
    random.shuffle(words)
    title = "".join(words) + kw
    tags = " ".join(["#" + kw, "#" + cat] + (["#" + random.choice(VIRAL)] if n_v else []))
    followers = int(math.exp(random.gauss(7, 1.5)))
    base = math.exp(random.gauss(4.5, 1.0)) * (1 + 1.2 * n_v)
    likes = int(base)
    collects = int(base * random.uniform(0.3, 1.2))
    comments = int(base * random.uniform(0.05, 0.3))
    rows.append({
        "note_id": f"demo{i:04d}", "category": cat, "title": title, "tags": tags,
        "content_snippet": "", "likes": likes, "collects": collects, "comments": comments,
        "author_followers": followers, "publish_date": "2026-10-01",
        "has_video": random.choice([0, 1]), "title_len": len(title), "label_viral": "",
    })

with open("data/notes_demo.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print("demo rows:", len(rows))
