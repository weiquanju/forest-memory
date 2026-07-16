#!/bin/bash
#
# setup_experiment.sh — 对照实验环境初始化脚本
#
# 使用 git worktree 为每个被测对象创建物理隔离的工作目录，支持并行实验。
# 脚本自动从 skill assets/input/ 复制实验资料，无需用户手动复制。
# 脚本会检查/初始化 git 仓库，创建实验目录结构，为每个 subject 创建独立 worktree。
#
# 用法:
#   bash setup_experiment.sh <project_name> <subject1> [subject2] [subject3] ...
#
# 示例:
#   bash setup_experiment.sh exp-model-20260716 dsv4flash dsv4pro glm52
#   bash setup_experiment.sh exp-tool-20260716 codebuddy qwen-codex claude-code
#   bash setup_experiment.sh exp-source-20260716 bim frs paper-2404-13501
#
# 前置条件:
#   - Git Bash（Windows）或 bash（Linux/macOS）
#   - Git 已安装 (2.6+)
#   - assets/input/ 目录已准备好输入资料（bim/frs/paper）
#
set -e

# 脚本所在目录（用于定位 assets/input/ 和模板文件）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_SOURCE="$SCRIPT_DIR/input"
METADATA_TEMPLATE_SOURCE="$SCRIPT_DIR/experiment_metadata_template.yaml"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC}  $1"; }

# ============================================================================
# 参数校验
# ============================================================================
if [ $# -lt 2 ]; then
    echo "用法: $0 <project_name> <subject1> [subject2] [subject3] ..."
    echo ""
    echo "示例:"
    echo "  $0 exp-model-20260716 dsv4flash dsv4pro glm52"
    echo "  $0 exp-tool-20260716 codebuddy qwen-codex claude-code"
    echo "  $0 exp-source-20260716 bim frs paper-2404-13501"
    exit 1
fi

PROJECT_NAME="$1"
shift
SUBJECTS=("$@")

log_info "实验项目: $PROJECT_NAME"
log_info "被测对象: ${SUBJECTS[*]}"
log_info "被测对象数量: ${#SUBJECTS[@]}"

if [ ${#SUBJECTS[@]} -lt 2 ]; then
    log_error "对照实验至少需要 2 个被测对象，当前只有 ${#SUBJECTS[@]} 个"
    exit 1
fi

# ============================================================================
# Step 1: 检查输入资料源
# ============================================================================
log_step "Step 1: 检查输入资料源 (assets/input/)"

if [ ! -d "$INPUT_SOURCE" ]; then
    log_error "输入资料源不存在: $INPUT_SOURCE"
    log_error "请在 skill assets/input/ 目录中放置实验资料（bim_source/frs_source/papers）"
    exit 1
fi

INPUT_OK=true

check_source() {
    local path="$1"
    local label="$2"
    if [ -d "$path" ] && [ -n "$(ls -A "$path" 2>/dev/null)" ]; then
        log_info "  ✓ $label: $path ($(ls "$path" | wc -l) 个文件)"
    else
        log_warn "  ✗ $label: $path (空或不存在)"
        INPUT_OK=false
    fi
}

check_source "$INPUT_SOURCE/bim_source"  "bim 源文档"
check_source "$INPUT_SOURCE/frs_source"  "frs 源文档"
check_source "$INPUT_SOURCE/papers"      "arXiv 论文"

if [ "$INPUT_OK" = false ]; then
    log_error "部分输入资料缺失，请补充后重试"
    log_error "  $INPUT_SOURCE/bim_source/  ← 人脑记忆机制的数据结构与算法分析.md"
    log_error "  $INPUT_SOURCE/frs_source/  ← AI与大模型...前沿研究综述.md"
    log_error "  $INPUT_SOURCE/papers/       ← 2404.13501.pdf (+ .md 基准文件)"
    exit 1
fi

# ============================================================================
# Step 2: 检查/初始化 Git 仓库
# ============================================================================
log_step "Step 2: 检查 Git 仓库"

if [ ! -d ".git" ]; then
    log_warn "当前目录不是 Git 仓库，自动初始化..."
    git init --initial-branch=main
    log_info "Git 仓库已初始化 (main 分支)"
else
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    log_info "Git 仓库已存在，当前分支: $CURRENT_BRANCH"
fi

# 确认 git worktree 可用
if ! git worktree list >/dev/null 2>&1; then
    log_error "git worktree 不可用，请检查 Git 版本 (需要 2.6+)"
    exit 1
fi
log_info "git worktree 可用"

# ============================================================================
# Step 3: 创建实验项目目录结构 + 复制输入资料
# ============================================================================
log_step "Step 3: 创建实验项目目录结构"

PROJECT_DIR="$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 创建共享目录
mkdir -p input reviews subjects

# 自动从 assets/input/ 复制实验资料（无需用户手动操作）
log_info "从 skill assets/input/ 复制实验资料..."
cp -r "$INPUT_SOURCE/bim_source"  input/
cp -r "$INPUT_SOURCE/frs_source"  input/
cp -r "$INPUT_SOURCE/papers"      input/

# 验证复制结果
COPIED_FILES=$(find input -type f | wc -l)
log_info "已复制 $COPIED_FILES 个文件到 input/"

# 创建 .gitignore（忽略临时文件和 worktree 产物）
cat > .gitignore << 'GITIGNORE'
# 实验临时文件
*.tmp
*.log
.DS_Store

# worktree 中的运行时产物（通过 worktree 分支单独管理）
subjects/*/.experiment_metadata.yaml
GITIGNORE

log_info "项目目录已创建: $PROJECT_DIR/"
log_info "  ├── input/          (共享输入资料，从 assets/input/ 自动复制)"
log_info "  ├── reviews/        (评审报告)"
log_info "  ├── subjects/       (worktree 根目录)"
log_info "  └── .gitignore"

# 提交输入资料到主分支（作为版本锁定基线）
git add -A
git commit -m "lock: input materials for experiment $PROJECT_NAME" --allow-empty 2>/dev/null || \
    log_info "输入资料已提交（或无变更）"

# ============================================================================
# Step 4: 为每个被测对象创建 git worktree
# ============================================================================
log_step "Step 4: 为每个被测对象创建 git worktree"

for subject in "${SUBJECTS[@]}"; do
    WORKTREE_PATH="subjects/$subject"
    BRANCH="experiment/$subject"

    log_info "创建 worktree: $subject"
    log_info "  路径: $WORKTREE_PATH"
    log_info "  分支: $BRANCH"

    # 检查 worktree 是否已存在
    if [ -d "$WORKTREE_PATH" ]; then
        log_warn "  worktree 已存在，跳过: $WORKTREE_PATH"
        continue
    fi

    # 检查分支是否已存在
    if git show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
        # 分支已存在，基于现有分支创建 worktree
        git worktree add "$WORKTREE_PATH" "$BRANCH"
        log_info "  ✓ worktree 已创建（基于现有分支）"
    else
        # 创建新分支并添加 worktree
        git worktree add "$WORKTREE_PATH" -b "$BRANCH"
        log_info "  ✓ worktree 已创建（新分支）"
    fi

    # 复制输入资料到 worktree（确保完全隔离，不依赖符号链接）
    mkdir -p "$WORKTREE_PATH/input"
    cp -r input/bim_source  "$WORKTREE_PATH/input/" 2>/dev/null || log_warn "  bim_source 复制失败"
    cp -r input/frs_source  "$WORKTREE_PATH/input/" 2>/dev/null || log_warn "  frs_source 复制失败"
    cp -r input/papers      "$WORKTREE_PATH/input/" 2>/dev/null || log_warn "  papers 复制失败"

    # 创建空的 forest/ 输出目录
    mkdir -p "$WORKTREE_PATH/forest"

    # 创建 worktree 级别的 .gitignore
    cat > "$WORKTREE_PATH/.gitignore" << 'WORKTREE_GITIGNORE'
# worktree 运行时产物
*.tmp
*.log
.DS_Store
WORKTREE_GITIGNORE

    log_info "  ✓ input/ 已复制（隔离副本）"
    log_info "  ✓ forest/ 已创建（空，待抽取）"
    echo ""
done

# ============================================================================
# Step 5: 生成实验元数据模板和各 worktree 元数据
# ============================================================================
log_step "Step 5: 生成实验元数据"

# 复制元数据模板到项目根目录
METADATA_TEMPLATE="$PROJECT_DIR/.experiment_metadata_template.yaml"
if [ -f "$METADATA_TEMPLATE_SOURCE" ]; then
    cp "$METADATA_TEMPLATE_SOURCE" "$METADATA_TEMPLATE"
    log_info "元数据模板已从 skill assets 复制"
else
    log_warn "元数据模板源不存在，创建基础模板"
    cat > "$METADATA_TEMPLATE" << 'METADATA'
experiment:
  project_name: ""
  dimension: ""          # model / tool / material
  created: ""
  status: in_progress

environment:
  tool_name: ""
  tool_version: ""
  ide_name: ""
  ide_version: ""
  os: ""
  node_version: ""

fixed_variables:
  model: ""
  tool: ""
  material: ""

subjects: []

results: []
METADATA
fi

# 为每个 worktree 生成元数据文件
for subject in "${SUBJECTS[@]}"; do
    WORKTREE_PATH="subjects/$subject"
    METADATA_FILE="$WORKTREE_PATH/.experiment_metadata.yaml"

    if [ ! -f "$METADATA_FILE" ]; then
        cat > "$METADATA_FILE" << METADATA
experiment:
  project_name: "$PROJECT_NAME"
  subject: "$subject"
  dimension: ""          # 待填写: model / tool / material
  created: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  status: not_started

environment:
  tool_name: ""
  tool_version: ""
  ide_name: ""
  ide_version: ""
  os: "$(uname -s) $(uname -r)"
  node_version: ""

extraction:
  tokens_consumed: 0
  duration_minutes: 0
  human_correction_rate: 0.0

review_results: []
METADATA
        log_info "  ✓ $subject/.experiment_metadata.yaml 已生成"
    fi
done

# ============================================================================
# Step 6: 生成实验说明 README
# ============================================================================
log_step "Step 6: 生成实验说明 README"

cat > "$PROJECT_DIR/README.md" << README
# 对照实验: $PROJECT_NAME

## 实验环境

- 创建时间: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- 隔离方式: git worktree（物理隔离）
- 被测对象: ${SUBJECTS[*]}
- 输入资料: 从 skill assets/input/ 自动复制

## 目录结构

\`\`\`
$PROJECT_NAME/
├── input/                  # 共享输入资料（从 assets/input/ 自动复制，锁定版本）
│   ├── bim_source/
│   ├── frs_source/
│   └── papers/
├── subjects/               # git worktree（每个被测对象独立隔离）
│   ├── ${SUBJECTS[0]}/    # worktree (branch: experiment/${SUBJECTS[0]})
│   │   ├── input/          # 输入资料副本（隔离）
│   │   ├── forest/          # 实验输出（待抽取）
│   │   └── .experiment_metadata.yaml
│   └── ...
├── reviews/                # 评审报告（交叉评审）
├── .experiment_metadata_template.yaml
└── README.md
\`\`\`

## 执行方式

### 串行执行

对每个被测对象依次在新会话中执行：

\`\`\`bash
# 1. 进入 worktree
cd subjects/${SUBJECTS[0]}

# 2. 在新会话中启动 AI 编程工具
# 3. 执行 forest-generation-methodology 9 步 SOP
# 4. 完成后 commit
git add -A && git commit -m "experiment: ${SUBJECTS[0]} extraction complete"

# 5. 切换到下一个 subject（新会话）
cd ../${SUBJECTS[1]}
\`\`\`

### 并行执行（推荐）

为每个被测对象打开独立终端 + 独立会话：

\`\`\`
终端 1: cd subjects/${SUBJECTS[0]}  → 启动会话 1
终端 2: cd subjects/${SUBJECTS[1]}  → 启动会话 2
终端 3: cd subjects/${SUBJECTS[2]}  → 启动会话 3
\`\`\`

每个会话只看到自己 worktree 的文件，物理隔离，无法抄袭。

## 防抄袭机制

- 每个 subject 在独立 git worktree 中工作
- worktree 间物理隔离，互不可见
- 新会话上下文干净清洁，不继承历史
- 禁止读取其他 worktree 的 forest/ 输出

## 清理 worktree

实验完成后清理 worktree：

\`\`\`bash
git worktree remove subjects/${SUBJECTS[0]}
git worktree remove subjects/${SUBJECTS[1]}
# 或批量清理:
# git worktree prune
\`\`\`
README

log_info "README.md 已生成"

# ============================================================================
# 完成
# ============================================================================
echo ""
echo "=============================================="
log_info "实验环境初始化完成!"
echo "=============================================="
echo ""
log_info "项目目录: $PROJECT_DIR/"
log_info "被测对象: ${SUBJECTS[*]}"
log_info "输入资料: $COPIED_FILES 个文件（从 assets/input/ 自动复制）"
echo ""
log_info "下一步:"
echo "  1. 为每个 subject 在独立终端+新会话中执行实验"
echo "     cd subjects/{subject}/ && [启动 AI 工具]"
echo "  2. 实验完成后执行交叉评审"
echo "  3. 汇总结果到 reviews/ 和 REPORT.md"
echo ""
log_info "git worktree 列表:"
git worktree list
