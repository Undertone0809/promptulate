import { defineConfig } from 'vitepress'
import { withPwa } from '@vite-pwa/vitepress'

// https://vitepress.dev/reference/site-config
export default withPwa(defineConfig({
  title: "Promptulate - Lightweight AI Native development framework",
  description: "🚀Lightweight Large language model automation and Autonomous Language Agents development framework. Build your LLM Agent Application in a pythonic way!",
  sitemap: {
    hostname: "https://promptulate.cn",
    transformItems: (items) => {
      return items.map(item => ({
        ...item,
        changefreq: 'weekly',
        priority: 0.8,
      }))
    }
  },
  head: [
    [
      'script',
      {
        defer: 'true',
        'data-website-id': '628f906e-71c9-4ad5-b0a0-ff86e778b861',
        src: 'https://umami.zeeland.top/script.js'
      }
    ],
    [
      'script',
      {
        defer: 'true',
        'data-website-id': '87a6bbc8-4134-4496-80d0-2f926075dd53',
        src: 'https://umami.zeeland.top/script.js'
      }
    ],
    ['link', { rel: 'icon', href: '/logo.ico' }],
    ['meta', { property: 'description', content: '🚀Lightweight Large language model automation and Autonomous Language Agents development framework. Build your LLM Agent Application in a pythonic way.' }],
    ['meta', { property: 'keywords', content: 'Promptulate, pne, LLM, Large language model, Autonomous Language Agents, development framework' }],
    ['meta', { property: 'og:site_name', content: 'Promptulate' }],
    ['meta', { property: 'og:url', content: 'https://www.promptulate.cn' }],
    ['meta', { property: 'og:title', content: 'Promptulate - Lightweight AI Native development framework' }],
    ['meta', { property: 'og:description', content: '🚀Lightweight Large language model automation and Autonomous Language Agents development framework. Build your LLM Agent Application in a pythonic way.' }],
    ['meta', { property: 'og:image', content: 'https://r2.zeeland.top/images/2024/09/e84b5053274f7f82d1645ad240f7727f.png' }],
    ['meta', { property: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { property: 'twitter:image', content: 'https://r2.zeeland.top/images/2024/09/e84b5053274f7f82d1645ad240f7727f.png' }],
    ['meta', { property: 'twitter:title', content: 'Promptulate' }],
    ['meta', { property: 'twitter:description', content: '🚀Lightweight Large language model automation and Autonomous Language Agents development framework. Build your LLM Agent Application in a pythonic way.' }],
    ['meta', { name: 'baidu-site-verification', content: 'codeva-NkjDCTdsXS' }],
    [
      'script',
      {
        async: 'true',
        src: 'https://www.googletagmanager.com/gtag/js?id=G-8K40Y823SC'
      }
    ],
    [
      'script',
      {},
      `window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-8K40Y823SC');`
    ],
  ],
  pwa: {
    manifest: {
      name: "Promptulate",
      short_name: "promptulate",
      theme_color: "#2b2a27",
      background_color: "#ffffff",
      display: "standalone",
      orientation: "portrait",
      scope: "/",
      start_url: "/",
      icons: [
        {
          src: "/logo.png",
          sizes: "192x192",
          type: "image/png",
          purpose: "maskable any"
        }
      ]
    },
  },
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/logo.png',
    search: {
      provider: 'local'
    },
    nav: [
      { text: 'Guide', link: '/get_started/intro' },
      { text: 'Use cases', link: '/use_cases/intro' }
    ],
    outline: {
      level: [2, 3],
    },
    sidebar: [
      {
        text: 'Get started',
        items: [
          { text: 'Introduction', link: '/get_started/intro' },
          { text: 'Quick Start', link: '/get_started/quick_start' },
          { text: 'How-to Guide', link: '/get_started/how-to-guide' }
        ]
      },
      {
        text: 'Use Cases',
        items: [
          { text: 'Best practices', link: '/use_cases/intro' },
          { text: 'Awesome chat function', link: '/use_cases/chat_usage' },
          { text: 'Build streamlit chatbot by pne', link: '/use_cases/streamlit-chatbot' },
          { text: 'Build gradio chatbot by pne', link: '/use_cases/gradio-chatbot' },
          { text: 'Personal Healing Assistant with mem0', link: '/use_cases/mem0-streamlit' },
          { text: 'Build math application with agent', link: '/use_cases/build-math-application-with-agent' },
          { text: 'Groq, llama3, Streamlit to build a application', link: '/use_cases/streamlit-groq-llama3' },
          { text: 'Build knowledge map with streamlit', link: '/use_cases/llmapper' },
          { text: 'Chat with GitHub repo', link: '/use_cases/chat-to-github-repo' },
          { text: 'Build Wechat-bot with itchat', link: '/use_cases/wx-chatbot' },
          { text: 'Combined with ToT in-depth reasoning Game24', link: '/use_cases/game24-with-tot' },
        ]
      },
      {
        text: 'Modules',
        items: [
          {
            text: 'Agent',
            link: '/modules/agent',
            items: [
              { text: 'Assistant Agent', link: '/modules/agents/assistant_agent_usage' }
            ]
          },
          {
            text: 'LLMs',
            link: '/modules/llm/llm',
            items: [
              { text: 'LLM Factory', link: '/modules/llm/llm-factory-usage' },
              { text: 'Custom LLM', link: '/modules/llm/custom_llm' },
              { text: 'OpenAI', link: '/modules/llm/openai' },
              { text: 'Erniebot 百度文心', link: '/modules/llm/erniebot' },
              { text: 'GLM 智谱AI', link: '/modules/llm/zhipu' }
            ]
          },
          {
            text: 'Tool',
            link: '/modules/tools/index',
            items: [
              { text: 'Custom Tool', link: '/modules/tools/custom_tool_usage' },
              { text: 'LangChain Tool Usage', link: '/modules/tools/langchain_tool_usage' }
            ]
          },
          { text: 'Structured Output', link: '/modules/formatter' },
          { text: 'Hook & Lifecycle', link: '/modules/hook' },
          { text: 'Memory', link: '/modules/memory' },
          { text: 'Client', link: '/modules/client' },
          { text: 'String Template', link: '/modules/other/string_template' },
          { text: 'Schema', link: '/modules/schema' },
          // { text: 'Framework', link: '/modules/framework' },
          // { text: 'Preset', link: '/modules/preset' }
        ],
        collapsed: true,
      },
      {
        text: 'Other',
        items: [
          { text: 'FAQ', link: '/other/faq' },
          { text: 'Release Version', link: '/other/update' },
          { text: 'Roadmap', link: '/other/plan' },
          { text: 'Developer guidance', link: '/other/contribution' },
          { text: 'Log system', link: '/other/log_system' },
          { text: 'How to write model name?', link: '/other/how_to_write_model_name' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/undertone0809/promptulate' },
      { icon: 'twitter', link: 'https://x.com/kfhedRk3lXofRIB' }
    ],
    footer: {
      message: 'Released under the Apache 2.0 License.',
      copyright: 'Copyright © 2023-present Zeeland'
    },
    // Add an edit link for each page
    editLink: {
      pattern: 'https://github.com/undertone0809/promptulate/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },
  }
}))
