# 快速开始

## 安装并准备环境

```bash
pip install -e .
```

可选依赖：

```bash
uv add "pne[openai]"
uv add "pne[anthropic]"
```

## 启动文档站点

```bash
cd docs
npm install
npm run docs:dev
```

访问 `http://localhost:4173`。

## 文档结构

本项目文档建议结构如下：

- `docs/index.md`：站点首页
- `docs/guide/`：入门、配置、运行示例
- `docs/advanced/`：高级用法与最佳实践

后续新增内容请按该目录持续扩展。
