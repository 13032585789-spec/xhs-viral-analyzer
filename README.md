# xhs-viral-analyzer

小红书笔记爆款预测与标题优化（进行中）。

## 目标
给定笔记的标题和标签，预测它在同类目里是否容易成为爆款，再生成并排序候选标题。

## 当前进度
- [x] 项目骨架与 baseline（字符 n-gram TF-IDF + 逻辑回归）
- [ ] 真实数据采集（2～3 个类目，先 200 条）
- [ ] BERT 微调对比
- [ ] 生成与排序闭环、Streamlit demo
- [ ] nanoGPT 小模型复现

## 用法
```
python3 src/gen_demo_data.py            # 合成演示数据，仅测试流程
python3 src/make_labels.py data/notes_demo.csv data/notes_demo_labeled.csv [--normalize]
python3 src/baseline.py data/notes_demo_labeled.csv
```

## 爆款标签
按类目内互动数（点赞+收藏+评论）的分位数定义，默认前 20% 为爆款。`--normalize` 用互动数除以粉丝数，削弱粉丝量影响。

## 数据说明
`data/notes_demo*.csv` 是合成数据，不代表真实结果。真实数据仅用于学习研究，不上传、不分发，也不收集用户个人信息。
