# News MCP Server for AI Agents | NewsAI

> A news intelligence layer for MCP clients - not just a thin wrapper around search or RSS.

**NewsAI** is a **news MCP server** that gives Claude, Cursor, VS Code Copilot, Windsurf, and any MCP-compatible AI agent instant access to real-time headlines and detailed news retrieval across **7 global regions**, **multiple languages**, and **any topic**.

If you are looking for a serious **news MCP**, this is built for production agent workflows: no scraping, no RSS parsing, no brittle site adapters - just a single MCP endpoint with structured tools that work out of the box.

[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Provider](https://img.shields.io/badge/Provider-NewzAI-green)](https://newzai.ai)

**Want to see it in action?** Try it live at [app.newzai.ai](https://app.newzai.ai).

---

## What This MCP Actually Does

Most "news MCP" offerings are thin wrappers around generic search or a single feed. NewsAI is positioned differently: **MCP is the interface, but the product value is the news retrieval layer behind it**.

Instead of forcing agents to browse raw pages or depend on vague web search results, NewsAI lets them ask for:

- **Top headlines** for a specific region
- **Topic coverage** from a predefined category like `TECHNOLOGY` or `BUSINESS`
- **Custom-topic retrieval** for any keyword or theme
- **Recency-constrained news** using `last_n_hours`
- **Multilingual retrieval** using standard language codes

That makes it useful as an **agent-facing news intelligence layer** for assistants, research systems, market monitoring, and live RAG pipelines.

---

## Why NewsAI Is Different

| Capability | Thin news wrapper | NewsAI |
| --- | --- | --- |
| MCP-native tool interface | Partial | Yes |
| Region-specific news retrieval | Usually limited | Yes |
| Language parameterization | Rare | Yes |
| Recency filtering | Usually no | Yes |
| Predefined category retrieval | Usually no | Yes |
| Arbitrary topic search | Partial | Yes |
| Structured agent-ready outputs | Inconsistent | Yes |
| OAuth onboarding for interactive clients | Rare | Yes |

---

## Architecture

```text
AI Agent / MCP Client
        |
        v
NewsAI MCP Server (Streamable HTTP)
        |
        +-- Google OAuth session
        +-- Tool selection + parameter validation
        +-- Region / language / topic / recency controls
        v
NewsAI retrieval layer
        |
        v
Structured news results for the agent
```

The important point is that **MCP is the delivery mechanism, not the entire product**. The server exposes a compact, agent-usable tool surface on top of a live news retrieval system that already understands regional scope, topic intent, and freshness constraints.

---

## Quick Setup

Add the NewsAI news MCP server to your MCP client configuration:

```json
{
  "mcpServers": {
    "newzai": {
      "type": "http",
      "url": "https://api.newzai.ai/mcp/"
    }
  }
}
```

> **Authentication required** - Uses Google OAuth. You will be prompted to sign in on first use. No API key management needed for interactive clients.

Works with **Claude Desktop**, **Cursor**, **VS Code Copilot**, **Windsurf**, and any MCP-compatible client.

---

## Supported Coverage

NewsAI's MCP server currently supports:

- **7 regions:** India, United States, United Kingdom, Japan, Australia, Canada, Germany
- **Multilingual retrieval:** English, Japanese, German, Hindi, and more via language codes
- **Two retrieval modes:** predefined categories and fully custom topic search
- **Freshness controls:** latest headlines or time-bounded search using `last_n_hours`

Supported region slugs:
`india`, `united-states`, `united-kingdom`, `japan`, `australia`, `canada`, `germany`

---

## MCP Tools

This news MCP server exposes three tools to your AI agent.

### `fetch_news_headlines`

Fetch the latest top news headlines for a region.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `region` | string | Yes | One of the supported regions |
| `language` | string | No | Output language code, default `en` |

**Best for:** fast situational awareness, briefing agents, "what happened today?" workflows.

**Example prompt:**
> Get me the latest headlines from India.

**Example response:**
```text
- 25th Amendment row: Can Trump be removed from office amid Iran war?
- Iran's 'lost the key' post offers comic relief amid global tension
- NASA's Artemis II Crew To Break Distance Record
- IPL 2026: KKR vs PBKS in danger from thunderstorm threat
...
```

### `search_news_predefined_category`

Fetch rich, detailed news articles for a well-known topic category.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `predefined_category` | enum | Yes | One of the predefined categories below |
| `region` | string | No | Region to fetch from, default `india` |
| `language` | string | No | Output language code, default `en` |
| `top_k` | int | No | Number of articles to return, default `20` |

**Available categories:** `TECHNOLOGY`, `BUSINESS`, `ENTERTAINMENT`, `SPORTS`, `WORLD`

**Best for:** stable agent workflows where category-level intent is known ahead of time.

**Example prompt:**
> What's happening in technology news in the US?

### `search_news_for_any_category`

Fetch news for any custom keyword or topic.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `category` | string | Yes | Any topic or keyword such as `"climate change"` or `"AI regulation"` |
| `region` | string | No | Region to fetch from, default `india` |
| `language` | string | No | Output language code, default `en` |
| `top_k` | int | No | Number of articles to return, default `20` |
| `last_n_hours` | int | No | Limit to recent news, for example `24` |

**Best for:** market intelligence, competitor tracking, live research, and long-tail topic discovery.

**Example prompts:**
> Find me news about electric vehicles in Japan from the last 24 hours.

> What are people saying about AI regulation this week?

> Search for startup funding news in the US.

---

## Technical Notes

- **Protocol:** [Model Context Protocol](https://modelcontextprotocol.io) over remote HTTP transport
- **Remote endpoint:** `https://api.newzai.ai/mcp/`
- **Manifest transport type:** `streamable-http`
- **Authentication:** Google OAuth 2.0
- **Client model:** interactive sign-in for MCP tools, no manual key rotation for end users
- **Query controls:** region, language, predefined category, `top_k`, and `last_n_hours`
- **Language handling:** standard language code input, useful for multilingual agent workflows
- **Tool design:** small, explicit tool surface rather than an overloaded generic search tool

This design is deliberate. For agents, predictable parameters are usually more valuable than a broad but underspecified endpoint. NewsAI keeps the tool contract tight enough for reliable tool selection while still covering the main retrieval patterns users actually need.

---

## Design Principles

- **Retrieval over generation:** the server provides live news retrieval; the LLM handles reasoning and synthesis on top
- **Agent-first interface:** tools are parameterized for model use, not for human dashboard browsing
- **Freshness at query time:** current news is fetched during inference instead of relying on stale model memory
- **Structured over brittle:** agents get tool outputs instead of scraping arbitrary web pages
- **Focused tool surface:** headlines, category search, and custom search cover most real news workflows cleanly

---

## Why Use a News MCP Instead of Web Search?

| Feature | NewsAI news MCP | Generic web search |
| --- | --- | --- |
| Structured, clean output | Yes | No |
| Region-specific retrieval | Yes | Partial |
| Language control | Yes | Limited |
| Recency filtering | Yes | Usually no |
| Works natively in MCP clients | Yes | No |
| Promptable by tool-aware agents | Yes | Partial |
| No page scraping in the client | Yes | No |

---

## Use Cases

This news MCP server is well-suited for:

- **AI news briefing agents** that generate live daily or hourly digests
- **Research assistants** that need current topic coverage on demand
- **Market intelligence workflows** that track companies, sectors, policy, or competitor mentions
- **Content systems** that ground writing in current events instead of stale model memory
- **Multilingual assistants** that fetch news in one language and reason or summarize in another
- **RAG pipelines** that need live news as external context during inference
- **Monitoring agents** that repeatedly query specific sectors, geographies, or emerging topics

---

## Authentication

This MCP server uses **Google OAuth 2.0**. On first connection your MCP client redirects you to a Google sign-in page. After authorization, the client maintains the session automatically.

For most users, this means:

- no API key copy-paste
- no local secret management
- lower setup friction for trying the server inside an MCP client

If you need API-key-based access for autonomous pipelines, contact [feedback@newzai.ai](mailto:feedback@newzai.ai).

---

## Client Configuration Examples

### Claude Desktop

```json
{
  "mcpServers": {
    "newzai": {
      "type": "http",
      "url": "https://api.newzai.ai/mcp/"
    }
  }
}
```

### Cursor

```json
{
  "mcpServers": {
    "newzai": {
      "type": "http",
      "url": "https://api.newzai.ai/mcp/"
    }
  }
}
```

### VS Code (Copilot / Continue)

```json
{
  "mcpServers": {
    "newzai": {
      "type": "http",
      "url": "https://api.newzai.ai/mcp/"
    }
  }
}
```

---

## Frequently Asked Questions

**What makes this different from a generic "news MCP"?**
Most alternatives behave like thin connectors. NewsAI is designed as a news intelligence layer for AI agents, with structured tools for headlines, category retrieval, custom-topic search, language selection, and recency filtering.

**Does this work with Claude?**
Yes. Add the MCP config to Claude Desktop and Claude can call the news tools whenever a prompt requires current events.

**Is there a free tier?**
Yes. It is free to use with Google sign-in. If you are building an autonomous agent or pipeline that needs API-key access instead of OAuth, contact [admin@newzai.ai](mailto:admin@newzai.ai).

**What regions are supported?**
India, United States, United Kingdom, Japan, Australia, Canada, and Germany.

**Can I fetch news in languages other than English?**
Yes. Pass a language code such as `ja`, `de`, or `hi` in the `language` parameter.

**Is this just web search inside MCP?**
No. The value is not just "news over MCP." The value is a tighter retrieval layer for live news, exposed through MCP in a form agents can use reliably.

---

## Links

- Website: [newzai.ai](https://newzai.ai)
- Live app: [app.newzai.ai](https://app.newzai.ai)
- API: [api.newzai.ai](https://api.newzai.ai)
- MCP server endpoint: [https://api.newzai.ai/mcp/](https://api.newzai.ai/mcp/)
- Model Context Protocol: [modelcontextprotocol.io](https://modelcontextprotocol.io)
