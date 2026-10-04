---
name: firecrawl
description: Crawling, mapping, and scraping websites into LLM-ready markdown using Firecrawl. Use when the user asks to crawl a website, scrape a page, map a site, or extract content from a URL.
---

# Firecrawl Skill

This skill guides the AI assistant on how to scrape, crawl, and map websites using the Firecrawl MCP server.

## Key Capabilities

1. **Scraping (`firecrawl_scrape`)**: Scrapes a single URL and returns clean markdown content. Bypasses anti-bot protections and handles JS rendering.
2. **Crawling (`firecrawl_crawl`)**: Crawls an entire website starting from a base URL, returning markdown content for all discovered pages.
3. **Mapping (`firecrawl_map`)**: Fast and credit-efficient discovery of all URLs on a website (returns a sitemap-like list of URLs).

## Usage Reference

### Single-Page Scraping
Use when you need the main content of a single page:
```javascript
// Example Tool Call
firecrawl_scrape({
  url: "https://example.com/page",
  formats: ["markdown"]
})
```

### Site Crawling
Use to audit or extract all pages from a site:
```javascript
// Example Tool Call
firecrawl_crawl({
  url: "https://example.com",
  limit: 50
})
```

### Site Mapping
Use to discover all pages on a site (returns a list of URLs):
```javascript
// Example Tool Call
firecrawl_map({
  url: "https://example.com"
})
```
