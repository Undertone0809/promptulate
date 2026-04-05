import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Promptulate',
  description: 'An SDK for REACT-style agents and tool integrations.',
  lang: 'zh-CN',
  srcDir: './',
  outDir: '.vitepress/dist',
  themeConfig: {
    logo: 'Promptulate',
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
    footer: {
      message: '基于 VitePress 构建，适配 Vercel 部署。',
      copyright: 'Copyright © 2026 Promptulate',
    },
    search: {
      provider: 'local',
    },
    socialLinks: [
      {
        icon: 'github',
        link: 'https://github.com/',
      },
    ],
  },
  markdown: {
    lineNumbers: true,
  },
})
