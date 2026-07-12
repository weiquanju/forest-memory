---
name: paper-review
description: >
  This skill automates structured academic paper reviews. It should be used when the user
  asks to "审稿", "review a paper", "论文审查", "audit a paper", "peer review", "论文审计",
  or provides an arXiv ID / paper title / DOI with intent to critically evaluate it.
  The skill orchestrates arxiv-mcp-server, GitHub MCP, web_fetch (DBLP/OpenAlex/OpenReview),
  and web_search to produce a multi-dimensional review report covering structural quality,
  technical soundness, cross-domain (human brain memory × CS/LLM) perspective, reproducibility,
  and a final recommendation.
---

# Paper Review — Structured Academic Paper Auditing

## Overview

This skill performs a comprehensive multi-stage academic paper review by orchestrating
available tools in parallel where possible. It covers: paper discovery and metadata
verification, citation analysis, venue/author credibility check, code reproducibility
audit, public review search, and cross-domain critique from the dual perspective of
human brain memory mechanisms and computer science / machine learning.

The output is a structured review report in markdown following a standard peer-review
format (Summary → Major Concerns → Minor Concerns → Recommendation).

## Workflow Decision Tree

```
User provides paper identifier
          │
          ├─ arXiv ID (e.g. 2301.12345) ──→ Phase 1: Quick Scan
          ├─ Paper title ────────────────→ Phase 1 (search arXiv first)
          └─ DOI ────────────────────────→ Phase 1 (search arXiv first)
                    │
                    ▼
           Phase 1: Quick Scan (parallel calls)
                    │
                    ▼
           Phase 2: Deep Review (parallel calls)
                    │
                    ▼
           Phase 3: Report Generation
```

## Phase 1: Quick Scan (Information Gathering)

**Goal**: Collect all paper metadata and external signals in parallel.

Execute all of the following simultaneously:

### 1.1 Locate and read paper on arXiv
- Call `arxiv-mcp-server.search_papers` with the paper title / ID
- Call `arxiv-mcp-server.get_abstract` for the found paper ID
- If available, call `arxiv-mcp-server.read_paper` to extract full text

### 1.2 Venue and author verification via DBLP
- Use `web_fetch` to call `https://dblp.org/search/publ/api?q=<paper_title>&format=json`
- Determine: conference/journal tier, author publication history, any retractions
- Flag: is this a top venue (NeurIPS/ICLR/ICML/ACL/CVPR/etc.) or a workshop / preprint-only?

### 1.3 Citation metrics via OpenAlex
- Use `web_fetch` to call `https://api.openalex.org/works?filter=title.search:<title>&select=id,doi,cited_by_count,publication_date,primary_location,authorships`
- Record: citation count, venue, year, author h-index indicators

### 1.4 Public review search via OpenReview
- Use `web_search` with query: `<paper_title> site:openreview.net`
- Extract: any public peer reviews, scores, and discussion threads

### 1.5 Code repository check via GitHub MCP
- Use `web_search` with query: `<paper_title> github`
- Use `GitHub.search_repositories` to find the official code repo if mentioned in the paper
- Check: stars, last commit date, open issues, README quality

### 1.6 Citation graph analysis
- Call `arxiv-mcp-server.citation_graph` for the paper ID
- Identify: key cited works, who cites this paper, research lineage

### Quick Scan Decision

After Phase 1, form a preliminary assessment:
- **Desk Reject signals**: obvious methodological flaws, known-vs-unknown venue, citation count = 0 after >1 year
- **Promising signals**: top venue, strong citations, public reviews positive, code available

If a desk-reject signal is strong and obvious, skip to Phase 3 with a brief justification.
Otherwise, proceed to Phase 2.

## Phase 2: Deep Review (Content Analysis)

**Goal**: Critically evaluate the paper's content against academic standards.

### 2.1 Structural Analysis
Read through Introduction, Related Work, Methodology, Experiments, and Conclusion.
Evaluate:

- **Problem definition**: Is the research question clearly stated? Is it meaningful?
- **Literature coverage**: Are key related works cited? Any glaring omissions?
- **Method clarity**: Could a peer reproduce the method from the description alone?
- **Experimental rigor**: Baselines reasonable? Ablation studies thorough? Statistical tests?

### 2.2 Technical Soundness Audit
- Identify any mathematical errors or unsupported claims
- Evaluate whether experiments actually prove the claimed contributions
- Check for overfitting to specific benchmarks (SOTA-chasing without insight)
- Check for appropriate statistical reporting (error bars, multiple runs, significance tests)

### 2.3 Cross-Domain Critique (Human Brain Memory × CS/LLM)

Load `references/review-criteria.md` and apply the cross-domain checklist.
Key questions to answer:

| Brain Memory Perspective | CS/LLM Counterpart |
|--------------------------|-------------------|
| Is the encoding mechanism biologically plausible? | Does the representation learning align with known neural coding principles? |
| Does the consolidation model match known neuroscience? | Is the memory/forgetting mechanism principled? How is catastrophic forgetting handled? |
| Is the retrieval process biologically grounded? | Does the attention/retrieval mechanism match hippocampus-cortex interaction models? |
| Is working memory analogy valid? | Is the attention mechanism truly analogous to biological working memory, or just superficial naming? |

### 2.4 Reproducibility Assessment
- Is code available and documented? (from Phase 1.5)
- Are hyperparameters fully specified?
- Are datasets publicly accessible?
- Any signs of "placeholder repo" (empty / incomplete code)?

## Phase 3: Report Generation

### 3.1 Compile Findings
Aggregate all observations from Phase 1 and Phase 2 into categories:
- Critical issues (block acceptance)
- Major concerns (require significant revision)
- Minor concerns (easily fixable)

### 3.2 Generate Report
Use the template structure from `assets/review-template.md`. The report MUST contain:

1. **Paper Summary** (2-3 sentences)
2. **Quick Facts Table**: venue, year, citations, code available (yes/no), public reviews (yes/no)
3. **Strengths** (bullet list)
4. **Major Concerns** (numbered, with section references)
5. **Minor Concerns** (numbered, with line/section references)
6. **Cross-Domain Audit Notes** (from Phase 2.3)
7. **Reproducibility Score** (1-5 scale with justification)
8. **Overall Recommendation**: Accept / Minor Revision / Major Revision / Reject, with confidence level (High/Medium/Low)

### 3.3 Deliver
Write the final report as a markdown file at the user's requested location, or output inline if no path is specified.

## Tool Call Optimization Rules

- **Phase 1**: ALL calls run in parallel (arxiv search + DBLP + OpenAlex + OpenReview search + GitHub + citation graph). No sequential dependency.
- **Phase 2**: Content reading is sequential (must read paper first), but load `references/review-criteria.md` in parallel with `arxiv-mcp-server.read_paper`.
- **Phase 3**: Pure composition — no external calls needed.
- Always use `web_search` as a fallback when direct API calls to DBLP/OpenAlex fail.

## References

- `references/review-criteria.md` — Detailed review dimensions, red flags checklist, and scoring rubric. Load this during Phase 2.3.

## Assets

- `assets/review-template.md` — Output template with placeholders. Use this as the report structure in Phase 3.2.
