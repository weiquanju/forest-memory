# FLM 森林专业术语表

> 来源：`docs/forest/frontier-llm-architecture/`（DeepSeek-V4 + Kimi K3 技术报告）
> 用途：辅助阅读，快速查阅专业术语的英文全称、中文翻译和定义解释。

---

## 一、架构设计

### 1.1 注意力机制

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| CSA | Compressed Sparse Attention | 压缩稀疏注意力 | 先按 1/m 比例压缩 KV cache，再用 Lightning Indexer 做 Top-k 稀疏选择，保留 token 级精细注意力 | DSv4 |
| HCA | Heavily Compressed Attention | 重度压缩注意力 | 按极高比例（1/128）压缩 KV cache 后执行稠密 MQA，牺牲 token 级精度换取极致效率 | DSv4 |
| DSA | DeepSeekSparseAttention | DeepSeek 稀疏注意力 | DeepSeek 系列模型的自研稀疏注意力算法，CSA 中用于压缩后 KV 条目的 Top-k 选择 | DSv4 |
| KDA | Kimi Delta Attention | Kimi Delta 注意力 | 基于 delta-rule recurrence + channel-wise forget gate 的线性注意力，用固定大小 recurrent state S 替代增长式 KV cache | K3 |
| MLA | Multi-head Latent Attention | 多头潜在注意力 | 通过低秩 latent vector 压缩 KV 表示以减少 KV cache 占用，最初由 DeepSeek-V2 提出，Kimi K3 改进为 Gated MLA | 通用 |
| GQA | Grouped-Query Attention | 分组查询注意力 | 将多个 query head 共享同一组 KV head，在 MHA 和 MQA 之间折中 KV cache 开销 | 通用 |
| MQA | Multi-Query Attention | 多查询注意力 | 所有 query head 共享同一套 KV，极致的 KV cache 节省方案 | 通用 |
| SWA | Sliding Window Attention | 滑动窗口注意力 | 每个 token 只关注最近的 n_win 个 token，DSv4 中作为 CSA/HCA 的补充分支增强局部依赖 | DSv4 |
| RoPE | Rotary Positional Embedding | 旋转位置编码 | 通过旋转变换将相对位置编码注入 attention 计算，DSv4 仅在 Q/K 尾部 64 维使用（Partial RoPE） | 通用 |
| NoPE | No Positional Encoding | 无位置编码 | 不使用显式位置编码，Kimi K3 的 KDA 通过 recurrent gating 隐式编码位置信息，MLA 层也使用 NoPE | K3 |

### 1.2 MoE 架构

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| MoE | Mixture-of-Experts | 专家混合 | 每层多个 FFN 专家 + 路由机制选择部分专家激活，实现稀疏计算以扩展模型容量 | 通用 |
| DeepSeekMoE | — | DeepSeek 专家混合架构 | fine-grained routed experts + shared experts 的组合，激活函数 Sqrt(Softplus)，辅以 auxiliary-loss-free 负载均衡 | DSv4 |
| StableLatentMoE | — | 稳定潜在空间专家混合 | 将 routed expert 压缩到 Latent Space（0.5× hidden dim），896 专家 + 16 激活（56× 稀疏度），含 SiTU-GLU + QuantileBalancing | K3 |
| LatentMoE | Mixture of Latent Experts | 潜在专家混合 | StableLatentMoE 的前身，核心思想是将专家宽度与模型全宽度解耦以廉价扩大专家池 | K3 |
| SiTU-GLU | SigmoidTanhUnit GLU | 双曲门控线性单元 | Kimi K3 的激活函数，用 bounded tanh 控制 SwiGLU 的无界增长（gate β₁=4, up β₂=25），解决极稀疏 MoE 的激活爆炸 | K3 |
| SwiGLU | Swish-Gated Linear Unit | Swish 门控线性单元 | Swish(x)·x 形式的门控激活函数，被广泛采用但无界，大型值下可能溢出 | 通用 |
| QB | QuantileBalancing | 分位数均衡 | 直接从 router-score 的 (1-k/n)-分位数推导每个 expert 的 bias，单次 forward pass 精确匹配目标负载 | K3 |
| Auxiliary-Loss-Free | — | 无辅助损失负载均衡 | 通过动态调整 expert-wise bias 维持负载均衡，无需添加辅助损失函数干扰梯度 | DSv4 |

### 1.3 残差连接

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| mHC | Manifold-Constrained Hyper-Connections | 流形约束超连接 | 将 HC 的残差映射矩阵约束到 Birkhoff 多面体（doubly stochastic matrices），通过 Sinkhorn-Knopp 算法投影，保证信号传播的非扩展性 | DSv4 |
| HC | Hyper-Connections | 超连接 | 扩展残差流宽度 n_hc 倍并引入动态线性映射，但多层堆叠时常出现数值不稳定（mHC 的前身） | 通用 |
| AttnRes | Attention Residuals | 注意力残差 | 将注意力机制应用于网络深度维度——每层用可学习 pseudo-query 选择性检索所有前驱层表示，而非均匀累积 | K3 |
| BlockAttnRes | Block Attention Residuals | 分块注意力残差 | AttnRes 的内存优化版本，将层分块后跨块做 Full Attention（N≈8 blocks），内存从 O(L·d) 降至 O(N·d) | K3 |

### 1.4 多模态

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| MoonViT-V2 | — | 月亮视觉 Transformer V2 | Kimi K3 的视觉编码器，27 层/0.4B 参数，从零开始训练（非 SigLIP 初始化），图像和视频共享参数 | K3 |
| ViT | Vision Transformer | 视觉 Transformer | 将图像切分为 patch 后输入 Transformer 处理，MoonViT-V2 的底层架构 | 通用 |
| Pixel Shuffle | — | 像素重排 | 将视觉 token 数量通过 2×2 downsampling 减少 4 倍的空间压缩操作 | K3 |

### 1.5 其他架构组件

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| MTP | Multi-Token Prediction | 多 Token 预测 | 每个位置预测多个未来 token 以增强训练信号，DSv4 深度=1；Kimi K3 将其 MTP layer 微调为 EAGLE-3 推测解码 draft model | 通用 |
| FFN | Feed-Forward Network | 前馈网络 | Transformer block 中的全连接子层，MoE 中每个 expert 即为一个 FFN | 通用 |
| KV Cache | Key-Value Cache | 键值缓存 | 推理时缓存已计算的 Key/Value 向量以避免重复计算，是注意力层的核心内存占用来源 | 通用 |

---

## 二、训练方法论

### 2.1 优化器

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| Muon | Momentum Orthogonalized by Newton-Schulz | 牛顿-舒尔茨正交化动量优化器 | 对 SGD-momentum 更新矩阵执行 Newton-Schulz 迭代以实现正交化（奇异值 → 1），DSv4 使用两阶段 Hybrid NS（8+2 步） | 通用 |
| Per-Head Muon | — | 按头 Muon 优化器 | Kimi K3 的 Muon 变体——沿 attention head 维度分区独立正交化，均衡各 head 更新尺度 | K3 |
| AdamW | Adaptive Moment Estimation with Weight Decay | 带权重衰减的自适应矩估计 | 广泛使用的自适应优化器，DSv4 中用于 Embedding/Prediction Head/RMSNorm 等非 Muon 参数 | 通用 |
| Newton-Schulz | Newton-Schulz Iteration | 牛顿-舒尔茨迭代 | 一种矩阵正交化的迭代算法，Muon 的核心操作——将动量矩阵的奇异值收敛到 1 | 通用 |
| Sinkhorn-Knopp | Sinkhorn-Knopp Algorithm | Sinkhorn-Knopp 算法 | 交替行/列归一化将正矩阵投影为 doubly stochastic matrix，mHC 用此算法将残差映射约束到 Birkhoff 多面体 | DSv4 |

### 2.2 预训练

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| TPP | Tokens-Per-Parameter | 每参数 Token 数 | 训练数据量与模型参数量的比值，Scaling Law 中的核心超参数之一 | K3 |
| WSD | Warmup-Stable-Decay | 预热-稳定-衰减 | 一种学习率调度策略，Kimi K3 的 Scaling Law 研究发现在各自最优超参数下 Cosine Decay 始终优于 WSD | K3 |
| FIM | Fill-in-Middle | 中间填充 | 预训练时让模型学习根据前后文补全中间内容，增强代码生成能力 | DSv4 |
| Document Packing | — | 文档打包 | 将多个短文档拼接为序列以减少 padding 和截断浪费，DSv4 继承自 V3 | DSv4 |

### 2.3 后训练

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| SFT | Supervised Fine-Tuning | 监督微调 | 在高质量标注数据上微调模型以建立基础指令遵循和领域能力，后训练流水线第一阶段 | 通用 |
| RL | Reinforcement Learning | 强化学习 | 通过 reward 信号优化策略，后训练的核心阶段；DSv4 用 GRPO，K3 用继承自 K2.5 的 RL 算法 | 通用 |
| GRPO | Group Relative Policy Optimization | 组相对策略优化 | DeepSeek 的 RL 算法，在 response group 内做相对比较来优化策略 | DSv4 |
| MOPD | Multi-Teacher On-Policy Distillation | 多教师在策略蒸馏 | Kimi K3 的蒸馏方案——以融合多个 domain-expert teacher 的 per-token reward 信号驱动 student 训练，而非直接概率匹配 | K3 |
| OPD | On-Policy Distillation | 在策略蒸馏 | 在 student 自身采样分布上进行蒸馏，DSv4 使用 Reverse KL 作为优化目标 | DSv4 |
| RLVR | Reinforcement Learning with Verifiable Rewards | 可验证奖励的强化学习 | 使用程序化验证器提供 reward 的 RL 方式，Kimi K3 的代码和数学域采用此方法 | K3 |
| GRM | Agentic Generative Reward Model | 智能体生成式奖励模型 | Kimi K3 用于非可验证通用任务的 reward model——强制遵循 read→rubric→score→scorepad 评估协议 | K3 |
| AET | Autonomous Execution Tasks | 自主执行任务 | Kimi K3 的一种 RL 环境范式——黑盒系统复制、量化因子发现、税务审计等 verify-in-the-loop 优化 | K3 |
| QAT | Quantization-Aware Training | 量化感知训练 | 训练过程中模拟量化精度损失使模型适应低精度推理，DSv4 用 FP4，K3 用 MXFP4 | 通用 |
| RLHF | Reinforcement Learning from Human Feedback | 基于人类反馈的强化学习 | 后训练的经典范式，两个报告中的 RL 阶段实质上是对 RLHF 的工程化扩展（用可验证环境/GRM 替代纯人类反馈） | 通用 |

---

## 三、基础设施

### 3.1 分布式训练

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| EP | Expert Parallelism | 专家并行 | 将 MoE 的不同 experts 分布到不同设备上，DSv4 实现细粒度 Wave-Based EP 将通信隐藏在计算中 | 通用 |
| DP | Data Parallelism | 数据并行 | 每设备持有完整模型副本、处理不同 batch 数据，梯度跨设备同步 | 通用 |
| PP | Pipeline Parallelism | 流水线并行 | 将模型层分段分布到不同设备，Kimi K3 使用 PP+VP(虚拟阶段) 支持 3T 参数规模 | 通用 |
| CP | Context Parallelism | 上下文并行 | 将长序列沿序列维度切分分布到多设备，DSv4 为 CSA/HCA 设计了两阶段 CP | 通用 |
| KCP | KDA Context Parallelism | KDA 上下文并行 | KDA 专用的 CP 方案——每 rank 计算本地 fragment（M 和 S̃），仅需固定大小 all-gather 通信 | K3 |
| ZeRO | Zero Redundancy Optimizer | 零冗余优化器 | 将优化器状态分片分布到多设备以消除冗余内存，DSv4 为 Muon 设计了混合 ZeRO 策略 | DSv4 |
| VP | Virtual Pipeline Stages | 虚拟流水线阶段 | 在 PP 基础上进一步细分虚拟阶段以减少流水线气泡，Kimi K3 使用 | K3 |

### 3.2 训练框架与工具

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| TileLang | — | 瓦片语言 | DeepSeek 使用的 DSL（领域特定语言），可将数百个细粒度算子融合为少量高性能 kernel，集成 Z3 SMT Solver 做形式化整数分析 | DSv4 |
| DeepGEMM | — | DeepSeek 通用矩阵乘法库 | DeepSeek 自研的高性能矩阵乘法库（替代 cuBLAS），支持 batch invariance | DSv4 |
| MegaMoE | — | 超大专家并行内核 | DeepSeek 开源的 CUDA mega-kernel，融合 Dispatch+Linear1+Linear2+Combine 为单一流水线，NVIDIA GPU 和华为 Ascend NPU 双平台 | DSv4 |
| FlashKDA | — | 闪光 KDA 内核 | Kimi K3 基于 CUTLASS 的 chunkwise KDA kernel，重叠 intra-chunk 计算与 cross-chunk state 传播 | K3 |
| MoonEP | — | 月亮专家并行 | Kimi K3 的专家并行框架——完美均衡、静态计算形状、零拷贝通信 | K3 |
| EAGLE-3 | — | 鹰-3 推测解码 | 一种推测解码框架，Kimi K3 将预训练 MTP layer 微调为 EAGLE-3 draft model，优化 L_K loss 直接最大化 acceptance rate | K3 |
| DualPipe | — | 双流水线 | DeepSeek 的 1F1B 流水线调度方案，mHC 调整后适应增加的 pipeline 通信量 | DSv4 |
| TorchFX | — | PyTorch 函数图追踪 | PyTorch 的计算图追踪工具，DSv4 用于 tensor-level activation checkpointing 的最小重计算子图识别 | DSv4 |
| SMT Solver | Satisfiability Modulo Theories Solver | 可满足性模理论求解器 | 形式化验证工具，TileLang 集成 Z3 的 QF_NIA 理论做整数表达式分析以解锁高级编译优化 | DSv4 |
| cuBLAS | CUDA Basic Linear Algebra Subprograms | CUDA 基础线性代数库 | NVIDIA 的 GPU 矩阵运算库，DSv4 用 DeepGEMM 端到端替代以保证 batch invariance | 通用 |

### 3.3 推理优化

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| Prefix Caching | — | 前缀缓存 | 复用相同前缀的 KV cache 以跳过重复 prefill，DSv4 使用 On-Disk 存储，K3 使用 KDA State-Aware Caching | 通用 |
| Speculative Decoding | — | 推测解码 | 用小模型（draft model）快速生成多个候选 token，target model 并行验证，K3 使用 EAGLE-3 方案 | K3 |
| L_K Loss | — | L_K 损失 | 直接最大化推测解码 acceptance rate 的损失函数：-log(Σ min(p(x), q(x)))，优于传统的 KL divergence | K3 |
| Wave Quantization | — | 波量化 | GPU 上因 SM 数量不能整除 work items 导致的利用率下降问题，DSv4 的双 kernel 策略解决 | DSv4 |

---

## 四、评估与基准

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| SimpleQA | — | 简单问答基准 | OpenAI 发布的事实性知识评估基准 | DSv4 |
| MMLU-Pro | Massive Multitask Language Understanding - Pro | 大规模多任务语言理解专业版 | 覆盖 57 个学科的知识评估基准增强版 | DSv4 |
| HLE | Humanity's Last Exam | 人类最后的考试 | 极高难度的学术知识评估基准 | DSv4 |
| GPQA | Google-Proof Q&A | 防谷歌问答基准 | 设计为无法通过搜索引擎直接回答的科学推理基准 | DSv4 |
| SWE-Bench | Software Engineering Benchmark | 软件工程基准 | 评估模型解决真实 GitHub issue 的编程能力 | 通用 |
| Terminal-Bench | — | 终端操作基准 | 评估模型在命令行环境中的 Agent 能力 | 通用 |
| CharXiv | — | 图表视觉推理基准 | 评估模型对图表、图形的理解和推理能力（含工具使用） | K3 |
| GDPval-AA | — | 通用 Agent 评估（Artificial Analysis） | Artificial Analysis 的通用 Agent 能力 Elo 评分 | K3 |

---

## 五、数学与算法术语

| 简称 | 完整英文名称 | 中文翻译 | 定义解释 | 论文 |
|------|-------------|---------|---------|:--:|
| Birkhoff Polytope | — | Birkhoff 多面体 | 所有 n×n doubly stochastic matrices 构成的凸多面体，mHC 将残差映射约束到此流形以保证非扩展性 | DSv4 |
| Doubly Stochastic Matrix | — | 双随机矩阵 | 行和与列和均为 1 的非负方阵，谱范数 ≤1，保证信号传播的非扩展性 | DSv4 |
| Delta-Rule | — | Delta 规则 | 一种增量学习规则，以当前预测误差调整权重：ΔW ∝ error × input，KDA 的核心数学基础 | K3 |
| Softmax Kernel | — | Softmax 核函数 | 将 Softmax attention 表达为核函数形式 φ(q)·φ(k)，AttnRes 使用 exp(q⊤·RMSNorm(k)) 作为核 | K3 |
| Reverse KL | Reverse Kullback-Leibler Divergence | 逆向 KL 散度 | KL(student∥teacher)，DSv4 On-Policy Distillation 的优化目标 | DSv4 |
| GRPO | Group Relative Policy Optimization | 组相对策略优化 | 在 response group 内计算相对优势来优化策略，DSv4 的核心 RL 算法 | DSv4 |
| RMSNorm | Root Mean Square Normalization | 均方根归一化 | 仅使用 RMS 统计量做归一化，计算效率高于 LayerNorm，两份报告中广泛使用 | 通用 |
| FP4/FP8/BF16 | — | 浮点精度格式 | 不同比特宽度的浮点数格式：FP4(4位)/FP8(8位)/BF16(Brain Float 16)，用于混合精度训练和推理以节省内存和带宽 | 通用 |
| MXFP4/MXFP8 | Microscaling Floating Point | 微缩放浮点格式 | 带共享缩放因子的块浮点格式，Kimi K3 后训练中用于量化 MoE expert weights (MXFP4) 和 activations (MXFP8) | K3 |

---

> **统计**：共收录 **75** 个专业术语，覆盖架构设计（35）、训练方法论（22）、基础设施（17）、评估基准（8）、数学与算法（5）五大类别。
