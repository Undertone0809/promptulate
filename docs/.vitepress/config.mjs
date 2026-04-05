import { defineConfig } from 'vitepress'

const repoUrl = 'https://github.com/Undertone0809/promptulate'

export default defineConfig({
  title: 'Promptulate',
  description:
    'Build your LLM Agent application in a Pythonic way with a lightweight SDK and modular agent components.',
  lang: 'zh-CN',
  srcDir: './',
  outDir: '.vitepress/dist',
  head: [
    ['link', { rel: 'icon', href: '/logo.ico' }],
    ['meta', { property: 'description', content: 'Build your LLM Agent application in a Pythonic way with a lightweight SDK and modular agent components.' }],
    ['meta', { property: 'keywords', content: 'Promptulate, pne, LLM, autonomous agents, tool integrations, AI agent sdk' }],
    ['meta', { property: 'og:site_name', content: 'Promptulate' }],
    ['meta', { property: 'og:title', content: 'Promptulate Docs' }],
    ['meta', { property: 'og:description', content: 'Build your LLM Agent application in a Pythonic way with a lightweight SDK and modular agent components.' }],
    ['meta', { property: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { property: 'twitter:title', content: 'Promptulate Docs' }],
    ['meta', { property: 'twitter:description', content: 'Build your LLM Agent application in a Pythonic way with a lightweight SDK and modular agent components.' }],
  ],
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'Promptulate',
    nav: [
      { text: '主页', link: '/' },
      { text: '快速开始', link: '/guide/getting-started' },
      { text: '使用说明', link: '/guide/usage' },
      { text: 'API', link: '/guide/configuration' },
      { text: 'GitHub', link: 'https://github.com/' },
    ],
    sidebar: [
      {
        text: '入门',
        items: [
          { text: '快速开始', link: '/guide/getting-started' },
          { text: '运行方式', link: '/guide/usage' },
          { text: '配置项', link: '/guide/configuration' },
        ],
      },
      {
        text: '高级',
        items: [
          { text: '示例与最佳实践', link: '/advanced/best-practices' },
        ],
      },
    ],
    outline: {
      level: [2, 3],
    },
    footer: {
      message: 'Prompts and agent docs for Promptulate.',
      copyright: 'Copyright © 2026 Promptulate',
    },
    editLink: {
      pattern: `${repoUrl}/edit/main/docs/:path`,
      text: '在 GitHub 上编辑此页',
    },
    search: {
      provider: 'local',
    },
    socialLinks: [
      {
        icon: 'github',
        link: repoUrl,
      },
    ],
  },
  markdown: {
    lineNumbers: true,
  },
})
