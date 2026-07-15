#!/usr/bin/env python3
"""
Knowledge Atom Extractor — 通用知识原子抽取脚本

从文档中利用 LLM 自动提取结构化知识原子，执行交叉声明检测，
并生成带 YAML Frontmatter 的 .md 文件。

Usage:
    # 单文件抽取
    python extract_knowledge.py --input doc.md --forest mke --output ./output

    # 批量目录抽取
    python extract_knowledge.py --input ./docs --forest mke --output ./output --recursive

    # 交叉声明检测（需要已有知识库）
    python extract_knowledge.py --input doc.md --forest mke --existing-db knowledge.db

    # 仅输出 JSON（不生成 .md）
    python extract_knowledge.py --input doc.md --forest mke --dry-run

Requirements:
    pip install openai pyyaml

Environment:
    OPENAI_API_KEY — OpenAI API key (required if using OpenAI backend)
    ANTHROPIC_API_KEY — Anthropic API key (required if using Anthropic backend)
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml")
    sys.exit(1)

try:
    import openai
except ImportError:
    openai = None  # Optional, error raised when used if missing


# ─── System Prompt ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
你是一个领域知识抽取专家。你的任务是从给定的文档中提取结构化的知识原子。

## 核心原则

1. **单一职责**：每个知识原子只能声明一个核心概念。如果原文包含多个独立概念，拆分为多个知识原子输出。
2. **引用而非重复**：如果检测到某个定义/标准在别处已有权威来源，输出引用关系而非重新声明。
3. **层级归属**：判断文档应归属的森林（forest）、树（tree）、枝干（branch）。
4. **元数据质量**：description 以核心价值为中心，不超过 120 字符。keywords 3-8 个。
5. **atom_type 判定**：semantic（事实）/ procedural（规则）/ episodic（经验）

## 输出 JSON Schema

{
  "extraction_meta": { "source_file": "", "source_hash": "", "extraction_model": "" },
  "atoms": [{
    "forest": "", "tree": "", "branch": "", "title": "",
    "description": "", "keywords": [], "atom_type": "semantic",
    "content_preview": "", "depends_on": []
  }],
  "references": [{
    "from_title": "", "to_forest": "", "to_title": "",
    "ref_type": "references", "keyword": ""
  }],
  "cross_declaration_warnings": [{
    "detected_in": "", "duplicates": "",
    "duplicate_type": "partial", "suggestion": "", "confidence": 0.0
  }]
}

## 质量要求

- description 不超过 120 字符，不含"本文档描述..."等无意义前缀
- keywords 至少 3 个，至多 8 个
- content_preview 不超过 200 字符
- 交叉声明不确定时也输出 warning（宁可多报，不可漏报）
"""


# ─── Core Functions ──────────────────────────────────────────────────────────

def compute_hash(text: str) -> str:
    """Compute SHA256 hash of text content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_from_document(
    doc_path: str,
    content: str,
    forest_hint: str,
    tree_hint: str | None,
    model: str,
    api_backend: str,
) -> dict:
    """
    Call LLM to extract knowledge atoms from a document.

    Returns the parsed JSON extraction result.
    """
    source_hash = compute_hash(content)

    user_prompt = f"""\
请从以下文档中提取结构化知识原子。

森林提示：{forest_hint}
树提示：{tree_hint or "（请自动判断）"}

## 文档内容

{content}
"""

    if api_backend == "anthropic":
        return _call_anthropic(user_prompt, model, doc_path, source_hash, forest_hint)
    else:
        return _call_openai(user_prompt, model, doc_path, source_hash, forest_hint)


def _call_openai(
    user_prompt: str, model: str, doc_path: str, source_hash: str, forest_hint: str
) -> dict:
    """Call OpenAI API for extraction."""
    if openai is None:
        raise ImportError("openai package is required: pip install openai")

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    result = json.loads(response.choices[0].message.content)
    result.setdefault("extraction_meta", {})
    result["extraction_meta"].update({
        "source_file": doc_path,
        "source_hash": source_hash,
        "extraction_model": model,
    })
    return result


def _call_anthropic(
    user_prompt: str, model: str, doc_path: str, source_hash: str, forest_hint: str
) -> dict:
    """Call Anthropic API for extraction."""
    try:
        import anthropic
    except ImportError:
        raise ImportError("anthropic package is required: pip install anthropic")

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = response.content[0].text
    # Extract JSON from response (may be wrapped in markdown code blocks)
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]

    result = json.loads(text.strip())
    result.setdefault("extraction_meta", {})
    result["extraction_meta"].update({
        "source_file": doc_path,
        "source_hash": source_hash,
        "extraction_model": model,
    })
    return result


# ─── Cross-Declaration Detection ──────────────────────────────────────────────

def load_existing_leaves(db_path: str) -> list[dict]:
    """Load existing leaves from SQLite database for cross-declaration detection."""
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, title, description, forest_id, tree_id, branch_id FROM leaf "
        "WHERE status != 'deprecated'"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def detect_cross_declarations(
    atoms: list[dict],
    existing_leaves: list[dict],
    threshold: float,
    embedding_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
) -> list[dict]:
    """
    Detect cross-declarations between candidate atoms and existing leaves.

    Uses vector embedding similarity (sentence-transformers) for semantic comparison.
    Default model is paraphrase-multilingual-MiniLM-L12-v2 for CJK text support.
    Falls back to keyword overlap if sentence-transformers is not available.

    Validated thresholds (from MKE 51-doc self-test with all-MiniLM-L6-v2):
      - > 0.85: very likely exact/partial duplicate (reject)
      - 0.80-0.85: likely index-vs-subdoc or semantic relation (review)
      - 0.55-0.80: semantic relatedness (normal in same-domain knowledge bases)
      - < 0.55: independent topics
    Note: multilingual model may produce different distributions; calibrate per corpus.
    """
    warnings = []

    # Try to use vector embeddings (preferred for CJK text)
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np

        model = SentenceTransformer(embedding_model_name)

        # Build embedding text for candidates
        cand_texts = []
        for atom in atoms:
            desc = atom.get("description", "")
            keywords = atom.get("keywords", [])
            cand_texts.append(f"{atom.get('title', '')}. {desc}. {' '.join(keywords)}")

        # Build embedding text for existing leaves
        leaf_texts = []
        for leaf in existing_leaves:
            desc = leaf.get("description") or ""
            leaf_texts.append(f"{leaf.get('title', '')}. {desc}")

        if not cand_texts or not leaf_texts:
            return warnings

        cand_vecs = model.encode(cand_texts, show_progress_bar=False, convert_to_numpy=True)
        leaf_vecs = model.encode(leaf_texts, show_progress_bar=False, convert_to_numpy=True)

        # Normalize for cosine similarity
        cand_norms = np.linalg.norm(cand_vecs, axis=1, keepdims=True)
        leaf_norms = np.linalg.norm(leaf_vecs, axis=1, keepdims=True)
        cand_normalized = cand_vecs / np.maximum(cand_norms, 1e-8)
        leaf_normalized = leaf_vecs / np.maximum(leaf_norms, 1e-8)

        # Compute cosine similarity matrix
        sim_matrix = cand_normalized @ leaf_normalized.T

        for i, atom in enumerate(atoms):
            for j, leaf in enumerate(existing_leaves):
                sim = float(sim_matrix[i, j])
                if sim > threshold:
                    leaf_title = leaf.get("title", "")
                    leaf_id = f"{leaf.get('forest_id', '')}:{leaf.get('tree_id', '')}:{leaf.get('branch_id', '')}:{leaf_title}"
                    dup_type = "exact" if sim > 0.95 else ("partial" if sim > 0.85 else "semantic")
                    warnings.append({
                        "detected_in": f"atom: {atom.get('title', '')}",
                        "duplicates": leaf_id,
                        "duplicate_type": dup_type,
                        "suggestion": f"请引用 [{leaf.get('forest_id', '')}] {leaf_title}，而非重复声明",
                        "confidence": round(sim, 2),
                    })

        return warnings

    except ImportError:
        pass  # Fall through to keyword-based detection

    # Fallback: keyword overlap (less accurate for CJK text)
    for atom in atoms:
        atom_keywords = set(atom.get("keywords", []))

        for leaf in existing_leaves:
            leaf_title = leaf.get("title", "")
            leaf_keywords = set()  # Existing leaves may not have keywords in DB

            # Simple keyword overlap
            if atom_keywords and leaf_keywords:
                overlap = atom_keywords & leaf_keywords
                sim = len(overlap) / max(len(atom_keywords | leaf_keywords), 1)
            else:
                sim = 0.0

            if sim > threshold:
                leaf_id = f"{leaf.get('forest_id', '')}:{leaf.get('tree_id', '')}:{leaf.get('branch_id', '')}:{leaf_title}"
                warnings.append({
                    "detected_in": f"atom: {atom.get('title', '')}",
                    "duplicates": leaf_id,
                    "duplicate_type": "partial" if sim < 0.95 else "exact",
                    "suggestion": f"请引用 [{leaf.get('forest_id', '')}] {leaf_title}，而非重复声明",
                    "confidence": round(sim, 2),
                })

    return warnings


# ─── Knowledge Atom Generation ───────────────────────────────────────────────

ATOM_TEMPLATE = """\
---
forest: {forest}
tree: {tree}
branch: {branch}
title: {title}
version: 1.0.0
created: {today}
updated: {today}
description: {description}
keywords:
{keywords_yaml}
atom_type: {atom_type}
status: draft
{depends_on_yaml}---

# {title}

{content}
"""


def generate_atom_md(atom: dict, content: str | None = None) -> str:
    """Generate a .md file for a knowledge atom with YAML frontmatter."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    keywords = atom.get("keywords", [])
    keywords_yaml = "\n".join(f"  - {kw}" for kw in keywords)

    depends_on = atom.get("depends_on", [])
    depends_on_yaml = ""
    if depends_on:
        depends_on_yaml = "depends_on:\n" + "\n".join(f"  - {d}" for d in depends_on) + "\n"

    body = content or atom.get("content_preview", atom.get("description", ""))

    return ATOM_TEMPLATE.format(
        forest=atom.get("forest", ""),
        tree=atom.get("tree", ""),
        branch=atom.get("branch", ""),
        title=atom.get("title", ""),
        today=today,
        description=atom.get("description", ""),
        keywords_yaml=keywords_yaml,
        atom_type=atom.get("atom_type", "semantic"),
        depends_on_yaml=depends_on_yaml,
        content=body,
    )


def safe_filename(title: str) -> str:
    """Convert a title to a safe filename."""
    # Replace unsafe characters
    safe = title.replace("/", "-").replace("\\", "-").replace(":", "-")
    safe = safe.replace(" ", "").replace("?", "").replace("*", "")
    return f"{safe}.md"


# ─── Main ────────────────────────────────────────────────────────────────────

def process_document(
    doc_path: str,
    forest: str,
    tree_hint: str | None,
    model: str,
    api_backend: str,
    output_dir: str,
    existing_db: str | None,
    threshold: float,
    dry_run: bool,
    embedding_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
) -> dict:
    """Process a single document: extract, detect, and optionally generate .md files."""
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 1: LLM extraction
    print(f"  Extracting: {doc_path}")
    result = extract_from_document(
        doc_path=doc_path,
        content=content,
        forest_hint=forest,
        tree_hint=tree_hint,
        model=model,
        api_backend=api_backend,
    )

    # Step 2: Cross-declaration detection
    if existing_db and os.path.exists(existing_db):
        existing_leaves = load_existing_leaves(existing_db)
        llm_warnings = result.get("cross_declaration_warnings", [])
        vector_warnings = detect_cross_declarations(
            result.get("atoms", []), existing_leaves, threshold, embedding_model_name
        )
        result["cross_declaration_warnings"] = llm_warnings + vector_warnings
        print(f"    Detected {len(result['cross_declaration_warnings'])} potential cross-declarations")

    # Step 3: Generate .md files
    if not dry_run:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        atoms = result.get("atoms", [])
        rejected = {w["detected_in"] for w in result.get("cross_declaration_warnings", [])
                    if "exact" in w.get("duplicate_type", "")}

        for atom in atoms:
            atom_key = f"atom: {atom.get('title', '')}"
            if atom_key in rejected:
                print(f"    Skipped (cross-declaration): {atom.get('title', '')}")
                continue

            md_content = generate_atom_md(atom)
            filename = safe_filename(atom.get("title", "untitled"))
            filepath = out / filename
            filepath.write_text(md_content, encoding="utf-8")
            print(f"    Generated: {filepath}")

    # Print warnings
    for w in result.get("cross_declaration_warnings", []):
        print(f"    WARNING: {w['suggestion']} (confidence: {w['confidence']})")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Knowledge Atom Extractor — 从文档中提取结构化知识原子"
    )
    parser.add_argument("--input", required=True, help="输入文件或目录路径")
    parser.add_argument("--forest", required=True, help="森林 ID（如 mke, backend）")
    parser.add_argument("--tree", default=None, help="树名称提示（可选）")
    parser.add_argument("--output", default="./output", help="输出目录")
    parser.add_argument("--model", default="gpt-4o", help="LLM 模型")
    parser.add_argument("--backend", default="openai", choices=["openai", "anthropic"],
                        help="API 后端")
    parser.add_argument("--existing-db", default=None, help="已有知识库 SQLite 路径（用于交叉声明检测）")
    parser.add_argument("--threshold", type=float, default=0.85, help="交叉声明检测阈值")
    parser.add_argument("--embedding-model", default="paraphrase-multilingual-MiniLM-L12-v2",
                        help="sentence-transformers 嵌入模型（默认多语言模型，对中文友好）")
    parser.add_argument("--exclude-index", action="store_true",
                        help="排除 index.md 索引文件（避免 index 与子文档的误报）")
    parser.add_argument("--dry-run", action="store_true", help="仅输出 JSON，不生成 .md 文件")
    parser.add_argument("--recursive", action="store_true", help="递归处理目录")
    parser.add_argument("--json-output", default=None, help="JSON 结果输出路径")
    args = parser.parse_args()

    input_path = Path(args.input)

    # Collect files to process
    if input_path.is_file():
        files = [str(input_path)]
    elif input_path.is_dir():
        pattern = "**/*.md" if args.recursive else "*.md"
        files = [str(f) for f in input_path.glob(pattern) if f.is_file()]
        if args.exclude_index:
            files = [f for f in files if not f.endswith("index.md")]
    else:
        print(f"Error: Input path does not exist: {input_path}")
        sys.exit(1)

    if not files:
        print(f"No .md files found in: {input_path}")
        sys.exit(1)

    print(f"Processing {len(files)} file(s)...")
    print(f"  Forest: {args.forest}")
    print(f"  Model: {args.model} ({args.backend})")
    if args.existing_db:
        print(f"  Cross-declaration DB: {args.existing_db}")
    print()

    all_results = []
    for filepath in files:
        result = process_document(
            doc_path=filepath,
            forest=args.forest,
            tree_hint=args.tree,
            model=args.model,
            api_backend=args.backend,
            output_dir=args.output,
            existing_db=args.existing_db,
            threshold=args.threshold,
            dry_run=args.dry_run,
            embedding_model_name=args.embedding_model,
        )
        all_results.append(result)
        print()

    # Save JSON results if requested
    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"JSON results saved to: {args.json_output}")

    # Summary
    total_atoms = sum(len(r.get("atoms", [])) for r in all_results)
    total_warnings = sum(len(r.get("cross_declaration_warnings", [])) for r in all_results)
    print(f"Done. Extracted {total_atoms} atoms, detected {total_warnings} cross-declaration warnings.")


if __name__ == "__main__":
    main()
