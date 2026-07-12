# Review Criteria — Detailed Dimensions & Red Flags

## 1. Structural Review Dimensions

### 1.1 Problem Definition (Weight: High)
- [ ] Research question clearly stated in abstract and introduction
- [ ] Problem significance justified (not just "interesting")
- [ ] Gap in literature explicitly identified
- [ ] Contribution claims match what is actually delivered

### 1.2 Literature Coverage (Weight: Medium)
- [ ] Key foundational works cited (not just recent papers)
- [ ] Negative/critical prior work acknowledged, not ignored
- [ ] No "citation cartel" patterns (excessive self-citation, clique citing)
- [ ] Recent related work (last 1-2 years) included

### 1.3 Methodological Clarity (Weight: High)
- [ ] Method described in sufficient detail for reproduction
- [ ] Design choices justified (not just "we use X")
- [ ] Hyperparameters fully specified with rationale
- [ ] Algorithm pseudocode or equivalent clarity provided

### 1.4 Experimental Rigor (Weight: High)
- [ ] Baselines are state-of-the-art and fairly tuned
- [ ] Multiple datasets / benchmarks used (no single-benchmark overfitting)
- [ ] Ablation studies isolate the contribution of each component
- [ ] Statistical significance tests reported (p-values, confidence intervals)
- [ ] Error bars / standard deviation shown across multiple random seeds
- [ ] Computational cost reported (training time, GPU hours, parameter count)

## 2. Technical Soundness Audit

### 2.1 Theory
- [ ] Mathematical derivations are correct (spot-check key equations)
- [ ] Assumptions explicitly stated and reasonable
- [ ] No circular reasoning (e.g., assuming the conclusion)
- [ ] Theorems properly scoped (no over-claiming)

### 2.2 Empirical Claims
- [ ] Results support the conclusions drawn
- [ ] Correlation not mistaken for causation
- [ ] Improvement magnitude practically meaningful (not just statistically significant)
- [ ] Failure cases discussed (not cherry-picked success)

### 2.3 SOTA-Chasing Detection
- [ ] Novel insight beyond "ensembling existing techniques"
- [ ] Ablation shows which component drives improvement
- [ ] Method generalizes beyond benchmark-specific tuning

## 3. Cross-Domain Checklist (Human Brain Memory × CS/LLM)

Use this section when the paper claims brain-inspired, neuro-symbolic, or memory-mechanism approaches.

### 3.1 Encoding (Representation Learning)
- Does the encoding mechanism map to known neural encoding principles (e.g., sparse coding, predictive coding, hierarchical processing)?
- If using "hippocampal indexing," is it consistent with the standard model of systems consolidation?
- Are neural plausibility claims backed by neuroscience citations, or just hand-waving?

### 3.2 Consolidation (Memory Formation)
- If the paper proposes a memory consolidation mechanism:
  - Does it model the complementary learning systems (hippocampus for rapid encoding, neocortex for slow integration)?
  - Is catastrophic forgetting addressed in a biologically meaningful way?
  - Is the sleep/replay mechanism (if mentioned) consistent with known replay phenomena?
- For LLM memory: does the approach distinguish working memory (attention context) from long-term memory (retrieval/RAG)?

### 3.3 Retrieval (Memory Access)
- If pattern completion / pattern separation is claimed:
  - Does it match the computational role of the dentate gyrus and CA3?
  - Is the similarity metric justified?
- For attention-based retrieval: is the key-value analogy to cortical-hippocampal interaction valid, or superficial?
- Are retrieval failures analyzed (false memories, interference)?

### 3.4 Working Memory vs. Attention
- Is "working memory" used as a metaphor or as a computational model?
- If metaphorical: is the mapping explicitly stated as such?
- If computational: does it respect known capacity limits (~4±1 chunks) and time-course constraints?
- For transformer attention: claiming it as "working memory" requires justification beyond "it attends to context"

### 3.5 Marr's Levels Test
For any brain-inspired claim, identify which level of analysis the analogy operates at:
- **Computational level**: What problem is being solved? (Strongest claim — hardest to validate)
- **Algorithmic level**: What representation and process? (Moderate claim — needs algorithmic mapping)
- **Implementational level**: What physical substrate? (Weakest claim — usually not applicable to CS)

### 3.6 Falsifiability
- Can the proposed brain-inspired model be tested against neural data?
- Would a neuroscience experiment invalidating the analogy also invalidate the CS contribution? (If yes, this is a risk; if no, the brain inspiration may be cosmetic)

## 4. Red Flags Checklist

Any of the following warrants extra scrutiny:

| Red Flag | Severity |
|----------|----------|
| Single benchmark evaluation, no cross-dataset validation | Major |
| No ablation study | Major |
| No comparison to relevant published baselines | Major |
| Cherry-picked baselines (weaker versions) | Critical |
| Missing error bars / no multiple runs | Major |
| Claims of "brain-inspired" with zero neuroscience citations | Major |
| Over-claiming: abstract says "SOTA by 10%" but tables show <1% | Critical |
| Code repo is empty or has only a README | Major |
| Citation count = 0 after >1 year on arXiv | Minor (but note it) |
| Excessive self-citation (>20% of references) | Minor |
| No discussion of limitations or failure cases | Major |
| Mathematical errors in key derivations | Critical |
| Uses correlation to imply causation | Major |

## 5. Scoring Rubric

### Overall Score (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Flawless. Novel, well-executed, well-written, reproducible. |
| 7-8  | Strong. Minor issues in writing or experiments, easily fixable. |
| 5-6  | Borderline. Potential value but significant concerns in method or experiments. |
| 3-4  | Weak. Major flaws that question the contribution. Needs complete rework. |
| 1-2  | Reject. Fundamentally flawed or trivial. |

### Reproducibility Score (1-5)

| Score | Criteria |
|-------|----------|
| 5 | Full code, data, and environment; one-command reproduction |
| 4 | Code available, documented, minor setup needed |
| 3 | Code partially available or poorly documented |
| 2 | Code placeholder or missing critical components |
| 1 | No code, insufficient method details to reproduce |
