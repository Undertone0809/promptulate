# Promptulate 文档

<script setup>
const features = [
  '轻量 SDK，支持 OpenAI 与 Anthropic',
  'REACT 风格 Agent 执行链路',
  '可插拔 Tool 与技能体系',
]
</script>

<h1 class="vp-doc"><strong>Promptulate</strong> 文档</h1>

> 面向应用接入的智能体基础库，支持可组合的适配器与工具生态。

## 你可以从这里开始

- [快速开始](/guide/getting-started)
- [运行方式](/guide/usage)
- [配置项](/guide/configuration)
- [最佳实践](/advanced/best-practices)

## 核心特性

<ul>
  <li v-for="item in features" :key="item">
    {{ item }}
  </li>
</ul>

## 约定

1. 所有文档以 Markdown 为主，必要时使用 MDX。
2. 示例代码按 `use_cases/` 下的 README 与运行入口同步维护。
3. 当行为依赖本机文件系统或环境变量时，在 `use_case` 层显式说明。

## 参与贡献

文档变更请优先修改对应 `docs/` 下的 Markdown 文件，便于版本化管理和预览。
