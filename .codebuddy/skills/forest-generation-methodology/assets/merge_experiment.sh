#!/bin/bash
#
# merge_experiment.sh — 合并各 worktree 实验结果到主分支
#
# 实验完成后，将各 worktree 分支的实验产出合并到主分支的 subjects/{subject}/ 目录。
# 生成结果模板（对照矩阵 + 报告模板）。
#
# 用法:
#   bash merge_experiment.sh
#
# 前置条件:
#   - 各 subject 的 worktree 实验已完成并 commit
#   - 在实验项目根目录运行
#
set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC}  $1"; }

# ============================================================================
# Step 1: 确认环境
# ============================================================================
log_step "Step 1: 确认环境"

if [ ! -d ".git" ]; then
    log_error "当前目录不是 Git 仓库"
    exit 1
fi

# 切换到主分支
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
if [ "$CURRENT_BRANCH" != "main" ]; then
    log_info "切换到 main 分支（当前: $CURRENT_BRANCH）"
    git checkout main
fi
log_info "当前分支: main"

# ============================================================================
# Step 2: 获取所有实验分支
# ============================================================================
log_step "Step 2: 发现实验分支"

SUBJECTS=$(git branch --list "experiment/*" | sed 's/[* ]//g' | sed 's/experiment\///')

if [ -z "$SUBJECTS" ]; then
    log_error "没有找到实验分支 (experiment/*)"
    log_error "请确认各 subject 的 worktree 实验已完成并 commit"
    exit 1
fi

SUBJECT_COUNT=$(echo "$SUBJECTS" | wc -l)
log_info "发现 $SUBJECT_COUNT 个实验分支:"
echo "$SUBJECTS" | while read subject; do
    log_info "  - $subject"
done

# ============================================================================
# Step 3: 修改 .gitignore（允许合并后追踪元数据文件）
# ============================================================================
log_step "Step 3: 更新 .gitignore"

if [ -f ".gitignore" ]; then
    # 移除 subjects/*/.experiment_metadata.yaml 忽略规则
    if grep -q "subjects/\*/\.experiment_metadata" .gitignore 2>/dev/null; then
        sed -i '/subjects\/\*\/\.experiment_metadata\.yaml/d' .gitignore
        log_info ".gitignore 已更新（移除元数据忽略规则）"
    else
        log_info ".gitignore 无需修改"
    fi
fi

# ============================================================================
# Step 4: 合并各 subject 的实验结果
# ============================================================================
log_step "Step 4: 合并实验结果到主分支"

MERGED_COUNT=0
TOTAL_MD=0

for subject in $SUBJECTS; do
    WORKTREE_PATH="subjects/$subject"

    if [ ! -d "$WORKTREE_PATH/forest" ]; then
        log_warn "  $subject: forest/ 不存在，跳过"
        continue
    fi

    # 统计 .md 文件数
    MD_COUNT=$(find "$WORKTREE_PATH/forest" -name "*.md" 2>/dev/null | wc -l)

    if [ "$MD_COUNT" -eq 0 ]; then
        log_warn "  $subject: forest/ 中没有 .md 文件，跳过"
        continue
    fi

    # 添加 forest/ 到主分支 index
    git add -f "$WORKTREE_PATH/forest/"

    # 添加 .experiment_metadata.yaml（如果存在）
    if [ -f "$WORKTREE_PATH/.experiment_metadata.yaml" ]; then
        git add -f "$WORKTREE_PATH/.experiment_metadata.yaml"
    fi

    # 添加 input/ 副本（如果存在）
    if [ -d "$WORKTREE_PATH/input" ]; then
        git add -f "$WORKTREE_PATH/input/"
    fi

    log_info "  [OK] $subject: $MD_COUNT 个 .md 文件已合并"
    MERGED_COUNT=$((MERGED_COUNT + 1))
    TOTAL_MD=$((TOTAL_MD + MD_COUNT))
done

if [ "$MERGED_COUNT" -eq 0 ]; then
    log_error "没有可合并的实验结果"
    exit 1
fi

log_info "合并: $MERGED_COUNT 个 subject, $TOTAL_MD 个 .md 文件"

# ============================================================================
# Step 5: 提交合并
# ============================================================================
log_step "Step 5: 提交合并结果"

git commit -m "merge: all subjects extraction complete

Merged $MERGED_COUNT subjects ($TOTAL_MD .md files):
$(echo "$SUBJECTS" | while read s; do echo "  - $s"; done)" --allow-empty

log_info "合并已提交到 main 分支"

# ============================================================================
# Step 6: 生成结果模板
# ============================================================================
log_step "Step 6: 生成结果模板"

mkdir -p results

# 对照矩阵模板
if [ ! -f "results/comparison-matrix-models.md" ]; then
    cat > "results/comparison-matrix-models.md" << 'MATRIX'
# 对照矩阵：不同模型

> 实验完成后填写此表格。评审数据来自 reviews/ 目录。

| 实验 ID | 模型 | AAI | D1:引用真实 | D2:引用准确 | D3:层级组织 | D4:批判分析 | D5:学术规范 | 综合 | 修正率 | 叶子数 | 树数 | 评审者 |
|---------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|------|
| exp-001 | dsv4flash | 40 | ? | ? | ? | ? | ? | ? | ? | ? | ? | dsv4pro, glm52 |
| exp-002 | dsv4pro | 44 | ? | ? | ? | ? | ? | ? | ? | ? | ? | dsv4flash, glm52 |
| exp-003 | glm52 | 51 | ? | ? | ? | ? | ? | ? | ? | ? | ? | dsv4flash, dsv4pro |

## 维度统计

### 叶子数对比

| 模型 | bim_source | frs_source | paper-2404.13501 | 总计 |
|------|:---:|:---:|:---:|:---:|
| dsv4flash | ? | ? | ? | ? |
| dsv4pro | ? | ? | ? | ? |
| glm52 | ? | ? | ? | ? |

### 树/枝干结构对比

| 模型 | 树数 | 枝干数 | 叶子数 | 平均每树叶子 |
|------|:---:|:---:|:---:|:---:|
| dsv4flash | ? | ? | ? | ? |
| dsv4pro | ? | ? | ? | ? |
| glm52 | ? | ? | ? | ? |
MATRIX
    log_info "results/comparison-matrix-models.md 已生成"
else
    log_info "results/comparison-matrix-models.md 已存在"
fi

# REPORT.md 模板
if [ ! -f "REPORT.md" ]; then
    cat > "REPORT.md" << 'REPORT'
# 对照实验报告

## 实验概述

- 实验维度：维度1（不同模型）
- 被测对象：dsv4flash (AAI 40), dsv4pro (AAI 44), glm52 (AAI 51)
- 输入资料：bim_source + frs_source + arXiv:2404.13501
- 隔离方式：git worktree（物理隔离）

## 对照数据

参见 [results/comparison-matrix-models.md](results/comparison-matrix-models.md)

## 关键发现

（待填写）

### 叶子数与 AAI 的关系

（待分析：AAI 分数高的模型是否产出更多/更少的叶子？）

### 树/枝干结构差异

（待分析：不同模型的森林组织方式有何差异？）

### 评审者偏差评估

（待分析：不同评审者对同一输出的评分差异如何？）

## 结论与局限

（待填写）
REPORT
    log_info "REPORT.md 已生成"
else
    log_info "REPORT.md 已存在"
fi

# ============================================================================
# Step 7: 合并结果统计
# ============================================================================
echo ""
echo "=============================================="
log_info "实验结果合并完成!"
echo "=============================================="
echo ""

log_info "合并统计:"
echo "  合并 subject 数: $MERGED_COUNT"
echo "  总 .md 文件数: $TOTAL_MD"
echo ""

log_info "各 subject 文件统计:"
for subject in $SUBJECTS; do
    WORKTREE_PATH="subjects/$subject"
    if [ -d "$WORKTREE_PATH/forest" ]; then
        MD_COUNT=$(find "$WORKTREE_PATH/forest" -name "*.md" 2>/dev/null | wc -l)
        TREE_COUNT=$(find "$WORKTREE_PATH/forest" -name "index.md" 2>/dev/null | wc -l)
        log_info "  $subject: $MD_COUNT .md / $TREE_COUNT index.md"
    fi
done
echo ""

log_info "下一步:"
echo "  1. 执行交叉评审（按交叉评审矩阵）"
echo "  2. 填写 results/comparison-matrix-models.md"
echo "  3. 完成 REPORT.md"
echo "  4. 清理 worktree:"
echo "     git worktree remove subjects/{subject}"
echo "     git worktree prune"
echo ""
log_info "git worktree 列表:"
git worktree list
