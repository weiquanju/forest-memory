# -*- coding: utf-8 -*-
"""
AGF MVP 抽取评估器

两种模式：
  [gold 模式，已弃用为主]  python evaluate.py <file.json> [<file2.json>]
      读 predictions.json（含 gold），算 D7 三元组命中率 + 约束召回率。
      注意：gold 由强模型设计，存在同源偏差，仅作机制演示。

  [agreement 模式]         python evaluate.py --agreement weak.json strong.json [strong2.json]
      不依赖 gold。比较不同模型对同一测试文本的抽取一致性。
      弱-强一致性显著低于强-强基线 -> H2 抽取侧依赖 D4 成立 (PASS)。
      注意：一致性是弱证据（一致性低仅说明"随模型变化"，不含方向）。

  [coverage 模式，强证]    python evaluate.py --coverage constraint_anchors.json m1.json m2.json ...
      读客观锚点(constraint_anchors.json 的 expected_constraint_keys)，
      算每个模型的约束覆盖率(recall)与过度抽取(幻觉约束)。
      方向明确：覆盖率随模型能力单调上升 -> H2 强证成立。
"""

import json
import sys


# ============================================================
# gold 模式（演示/历史保留）
# ============================================================
def d7(sample):
    gold, preds = sample["gold"], sample.get("preds", [])
    triple_hit = any(
        p["s"] == gold["s"] and p["p"] == gold["p"] and p["o"] == gold["o"]
        for p in preds
    )
    gk = set(gold.get("constraints", {}).keys())
    pk = set()
    for p in preds:
        if p["s"] == gold["s"] and p["p"] == gold["p"]:
            pk |= set(p.get("constraints", {}).keys())
    c_recall = (len(gk & pk) / len(gk)) if gk else 1.0
    return triple_hit, c_recall


def report(path):
    data = json.load(open(path, encoding="utf-8"))
    hits, recs, hard_recs = [], [], []
    for s in data["samples"]:
        th, cr = d7(s)
        hits.append(th)
        recs.append(cr)
        if s["gold"].get("constraints"):
            hard_recs.append(cr)
    n = len(data["samples"])
    tr, ar, hr = sum(hits) / n, sum(recs) / n, (sum(hard_recs) / len(hard_recs) if hard_recs else 1.0)
    print(f"模型: {data.get('model', '?')}")
    print(f"  样本数: {n}")
    print(f"  三元组命中率: {tr:.0%}")
    print(f"  约束召回率(constraint_recall): {ar:.0%}")
    print(f"  难样本约束召回率: {hr:.0%}")
    return tr, ar, hr


# ============================================================
# agreement 模式（主用）：跨模型一致性
# ============================================================
def triple_set(preds):
    return set((p.get("s"), p.get("p"), p.get("o")) for p in preds)


def constraint_of(preds):
    return {(p.get("s"), p.get("p"), p.get("o")): p.get("constraints", {}) for p in preds}


def pair_agreement(a_preds, b_preds):
    """对一条文本的两次抽取，算一致性。返回 (triple_agree, constraint_agree)。"""
    ta, tb = triple_set(a_preds), triple_set(b_preds)
    triple_agree = (ta == tb)
    # 约束一致：两侧三元组集合相同，且每个三元组的 constraints 相等
    ca, cb = constraint_of(a_preds), constraint_of(b_preds)
    constraint_agree = (ca == cb)
    return triple_agree, constraint_agree


def agreement_mode(files):
    datas = [json.load(open(f, encoding="utf-8")) for f in files]
    n = len(datas[0]["samples"])
    # 对齐：假设各文件 samples 同序同 text
    pair_results = []
    for i in range(len(datas) - 1):
        ta, tb = datas[i], datas[i + 1]
        tris, cons = [], []
        for j in range(n):
            ag, cg = pair_agreement(ta["samples"][j]["preds"], tb["samples"][j]["preds"])
            tris.append(ag)
            cons.append(cg)
        pair_results.append({
            "a": ta.get("model", files[i]),
            "b": tb.get("model", files[i + 1]),
            "triple_agree": sum(tris) / n,
            "constraint_agree": sum(cons) / n,
            "n": n,
        })

    print("=" * 56)
    print("跨模型一致性评估 (inter-model agreement)")
    print("=" * 56)
    for r in pair_results:
        print(f"\n  {r['a']}")
        print(f"    vs {r['b']}")
        print(f"    三元组一致性: {r['triple_agree']:.0%}")
        print(f"    约束一致性:   {r['constraint_agree']:.0%}")

    # 判定：若提供 >=3 个文件，约定最后两个为强-强基线，第一个为弱
    if len(pair_results) >= 2:
        weak_strong = pair_results[0]      # files[0] vs files[1]
        strong_strong = pair_results[-1]   # 最后一对
        print("-" * 56)
        h2_pass = weak_strong["constraint_agree"] < strong_strong["constraint_agree"]
        print(f"  H2 抽取侧依赖 D4: [{'PASS' if h2_pass else 'FAIL'}]")
        print(f"    弱-强约束一致性 {weak_strong['constraint_agree']:.0%} "
              f"< 强-强约束一致性 {strong_strong['constraint_agree']:.0%}")
    elif len(pair_results) == 1:
        r = pair_results[0]
        print("-" * 56)
        h2_pass = r["constraint_agree"] < 1.0
        print(f"  H2 抽取侧依赖 D4: [{'PASS' if h2_pass else 'FAIL'}] "
              f"(无强-强基线；约束一致性<100%即视为存在能力依赖)")
        print(f"    约束一致性: {r['constraint_agree']:.0%}")


# ============================================================
# coverage 模式（强证）：对客观锚点算约束覆盖率 + 过度抽取
# ============================================================
def pred_constraint_keys(preds):
    """一条文本下所有 preds 的 constraints 键并集。"""
    keys = set()
    for p in preds:
        keys |= set(p.get("constraints", {}).keys())
    return keys


def coverage_mode(anchor_file, model_files):
    anchors = json.load(open(anchor_file, encoding="utf-8"))["anchors"]
    anchor_map = {a["text"]: set(a["expected_constraint_keys"]) for a in anchors}
    total_expected = sum(len(v) for v in anchor_map.values())

    print("=" * 56)
    print("约束覆盖率评估 (coverage vs 客观锚点)")
    print("=" * 56)
    print(f"锚点文本数: {len(anchor_map)}，期望约束键总数: {total_expected}")

    results = []
    for f in model_files:
        data = json.load(open(f, encoding="utf-8"))
        hit_keys = 0            # 命中的期望键计数 (micro recall 分子)
        over_extract = 0        # 对 expected=[] 文本抽出的幻觉约束键计数
        matched = 0             # 成功按 text 对齐的样本数
        for s in data["samples"]:
            text = s["text"]
            if text not in anchor_map:
                continue
            matched += 1
            expected = anchor_map[text]
            got = pred_constraint_keys(s.get("preds", []))
            hit_keys += len(got & expected)
            # v2.1 修订: 任何非期望键都计入 over_extract (覆盖 expected≠[] 文本的超额抽取)
            # 原版仅统计 expected=[] 的"无中生有",会漏掉 expected≠[] 时的"超额补全"
            over_extract += len(got - expected)
        recall = (hit_keys / total_expected) if total_expected else 1.0
        results.append({
            "model": data.get("model", f),
            "recall": recall,
            "hit": hit_keys,
            "over": over_extract,
            "matched": matched,
        })

    for r in results:
        print(f"\n  {r['model']}")
        print(f"    约束覆盖率(recall): {r['recall']:.0%}  ({r['hit']}/{total_expected})")
        print(f"    过度抽取(幻觉约束键): {r['over']}")
        print(f"    对齐样本数: {r['matched']}/{len(anchor_map)}")

    # H2 强证判定：覆盖率是否随能力单调上升（假设 model_files 已按能力升序传入）
    if len(results) >= 2:
        print("-" * 56)
        recalls = [r["recall"] for r in results]
        monotonic = all(recalls[i] <= recalls[i + 1] for i in range(len(recalls) - 1))
        spread = recalls[-1] - recalls[0]
        h2_pass = (recalls[0] < recalls[-1])
        print(f"  H2 抽取侧依赖 D4: [{'PASS' if h2_pass else 'FAIL'}]")
        print(f"    最弱覆盖率 {recalls[0]:.0%} < 最强覆盖率 {recalls[-1]:.0%} "
              f"(差 {spread:.0%})")
        print(f"    单调递增(按传入顺序): {'是' if monotonic else '否'}")
        print("    说明: 需按能力升序传入模型文件(弱->强)，方向锚定质量随能力上升。")


def main():
    args = sys.argv[1:]
    if "--coverage" in args:
        files = [a for a in args if a != "--coverage"]
        if len(files) < 2:
            print("coverage 模式: --coverage constraint_anchors.json m1.json [m2.json ...]")
            return
        coverage_mode(files[0], files[1:])
    elif "--agreement" in args:
        files = [a for a in args if a != "--agreement"]
        if len(files) < 2:
            print("agreement 模式需至少 2 个文件: --agreement weak.json strong.json [strong2.json]")
            return
        agreement_mode(files)
    elif len(args) >= 2:
        report(args[0])
        report(args[1])
        print("-" * 40)
        print("  (gold 模式仅演示；建议改用 --agreement 跨模型一致性)")
    elif len(args) == 1:
        report(args[0])
    else:
        print("用法:")
        print("  python evaluate.py <file.json>                          # gold 模式单点")
        print("  python evaluate.py --agreement w.json s.json [s2.json]  # 一致性模式(弱证)")
        print("  python evaluate.py --coverage anchors.json m1.json ...  # 覆盖率模式(强证)")


if __name__ == "__main__":
    main()
