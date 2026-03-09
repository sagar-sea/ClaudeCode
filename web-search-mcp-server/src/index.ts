#!/usr/bin/env node
/**
 * MCP Server for Web Search and Content Fetching.
 *
 * This server provides tools to search the web using Google Custom Search API
 * and fetch content from specific URLs with content extraction.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios, { AxiosError } from "axios";
import * as cheerio from "cheerio";

// Constants
const GOOGLE_SEARCH_API_URL = "https://www.googleapis.com/customsearch/v1";
const CHARACTER_LIMIT = 25000;

// Enums
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

// Zod schemas for input validation
const SearchInputSchema = z.object({
  query: z.string()
    .min(2, "Query must be at least 2 characters")
    .max(200, "Query must not exceed 200 characters")
    .describe("Search query string"),
  limit: z.number()
    .int()
    .min(1)
    .max(10)
    .default(5)
    .describe("Maximum number of search results to return (1-10)"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("Output format: 'markdown' for human-readable or 'json' for machine-readable")
}).strict();

type SearchInput = z.infer<typeof SearchInputSchema>;

const FetchUrlInputSchema = z.object({
  url: z.string()
    .url("Invalid URL format")
    .describe("URL to fetch content from"),
  extract_text: z.boolean()
    .default(true)
    .describe("Whether to extract main text content (removes HTML markup)"),
  max_length: z.number()
    .int()
    .min(100)
    .max(10000)
    .default(2000)
    .describe("Maximum length of extracted text (characters)"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("Output format: 'markdown' for human-readable or 'json' for machine-readable")
}).strict();

type FetchUrlInput = z.infer<typeof FetchUrlInputSchema>;

// Shared utility functions
async function makeApiRequest<T>(
  url: string,
  method: "GET" | "POST" = "GET",
  params?: Record<string, any>
): Promise<T> {
  try {
    const response = await axios({
      method,
      url,
      params,
      timeout: 30000,
      headers: {
        "User-Agent": "MCP-Web-Search-Server/1.0.0",
        "Accept": "application/json"
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}

function handleApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response) {
      switch (error.response.status) {
        case 400:
          return "Error: Bad request. Please check your parameters.";
        case 401:
          return "Error: Authentication failed. Check your API key.";
        case 403:
          return "Error: Permission denied. Check your API key permissions.";
        case 404:
          return "Error: Resource not found.";
        case 429:
          return "Error: Rate limit exceeded. Please wait before making more requests.";
        case 500:
          return "Error: Server error. Please try again later.";
        default:
          return `Error: API request failed with status ${error.response.status}`;
      }
    } else if (error.code === "ECONNABORTED") {
      return "Error: Request timed out. Please try again.";
    } else if (error.code === "ENOTFOUND") {
      return "Error: Cannot connect to the server. Check your internet connection.";
    }
  }
  return `Error: Unexpected error occurred: ${error instanceof Error ? error.message : String(error)}`;
}

function extractMainText(html: string, maxLength: number): string {
  try {
    const $ = cheerio.load(html);

    // Remove script and style elements
    $('script, style, nav, header, footer').remove();

    // Get text content
    let text = $('body').text();

    // Clean up the text
    text = text.replace(/\s+/g, ' ').trim();

    // Truncate if necessary
    if (text.length > maxLength) {
      text = text.substring(0, maxLength) + '... [content truncated]';
    }

    return text;
  } catch (error) {
    return "Error: Unable to extract text content from the page.";
  }
}

function truncateResponse(text: string): string {
  if (text.length > CHARACTER_LIMIT) {
    return text.substring(0, CHARACTER_LIMIT) + '\n\n[Response truncated due to size limits]';
  }
  return text;
}

// Create MCP server instance
const server = new McpServer({
  name: "web-search-mcp-server",
  version: "1.0.0"
});

// Register web search tool
server.registerTool(
  "web_search",
  {
    title: "Search the Web",
    description: `Search the web using Google Custom Search API.

This tool performs web searches and returns relevant results with titles, URLs, and snippets.

Requirements:
- GOOGLE_SEARCH_API_KEY environment variable must be set
- GOOGLE_SEARCH_ENGINE_ID environment variable must be set

Args:
- query (string): Search query string (2-200 characters)
- limit (number): Number of results (1-10, default: 5)
- response_format ('markdown' | 'json'): Output format (default: 'markdown')

Returns:
For JSON format:
{
  "total_results": number,
  "search_time": number,
  "items": [
    {
      "title": string,
      "link": string,
      "snippet": string,
      "display_link": string
    }
  ]
}

Examples:
- Search for "latest AI developments" -> params with query="latest AI developments"
- Search for "Python documentation" with 3 results -> params with query="Python documentation", limit=3

Error Handling:
- Returns authentication errors if API keys are missing or invalid
- Returns rate limit errors if quota exceeded
- Returns timeout errors if connection fails`,
    inputSchema: SearchInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: true
    }
  },
  async (params: SearchInput) => {
    try {
      // Check required environment variables
      const apiKey = process.env.GOOGLE_SEARCH_API_KEY;
      const searchEngineId = process.env.GOOGLE_SEARCH_ENGINE_ID;

      if (!apiKey || !searchEngineId) {
        return {
          content: [{
            type: "text",
            text: "Error: Missing required environment variables. Please set GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID."
          }]
        };
      }

      // Make search request
      const searchData = await makeApiRequest<any>(GOOGLE_SEARCH_API_URL, "GET", {
        key: apiKey,
        cx: searchEngineId,
        q: params.query,
        num: params.limit
      });

      const items = searchData.items || [];
      const totalResults = searchData.searchInformation?.totalResults || 0;
      const searchTime = searchData.searchInformation?.searchTime || 0;

      // Prepare structured output
      const output = {
        total_results: parseInt(totalResults) || 0,
        search_time: parseFloat(searchTime) || 0,
        items: items.map((item: any) => ({
          title: item.title || "No title",
          link: item.link || "",
          snippet: item.snippet || "No snippet available",
          display_link: item.displayLink || ""
        }))
      };

      // Format text representation based on requested format
      let textContent: string;
      if (params.response_format === ResponseFormat.MARKDOWN) {
        if (items.length === 0) {
          textContent = `# Search Results: "${params.query}"\n\nNo results found.`;
        } else {
          const lines = [
            `# Search Results: "${params.query}"`,
            ``,
            `Found approximately ${totalResults} results in ${searchTime} seconds`,
            ``
          ];

          items.forEach((item: any, index: number) => {
            lines.push(`## ${index + 1}. ${item.title}`);
            lines.push(`**URL**: ${item.link}`);
            if (item.displayLink) {
              lines.push(`**Site**: ${item.displayLink}`);
            }
            lines.push(`**Snippet**: ${item.snippet}`);
            lines.push(``);
          });

          textContent = lines.join("\n");
        }
      } else {
        textContent = JSON.stringify(output, null, 2);
      }

      // Apply character limit
      textContent = truncateResponse(textContent);

      return {
        content: [{ type: "text", text: textContent }],
        structuredContent: output
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: handleApiError(error)
        }]
      };
    }
  }
);

// Register URL content fetching tool
server.registerTool(
  "fetch_url_content",
  {
    title: "Fetch URL Content",
    description: `Fetch and extract content from a specific URL.

This tool downloads content from a given URL and optionally extracts the main text content by removing HTML markup.

Args:
- url (string): URL to fetch content from
- extract_text (boolean): Whether to extract main text (default: true)
- max_length (number): Maximum text length (100-10000, default: 2000)
- response_format ('markdown' | 'json'): Output format (default: 'markdown')

Returns:
For JSON format (when extract_text=true):
{
  "url": string,
  "title": string,
  "content": string,
  "content_length": number,
  "extracted": boolean
}

For JSON format (when extract_text=false):
{
  "url": string,
  "content": string,
  "content_length": number,
  "extracted": boolean
}

Examples:
- Fetch content from a news article -> params with url="https://example.com/article"
- Get raw HTML from a page -> params with url="https://example.com", extract_text=false

Error Handling:
- Returns error for invalid URLs
- Returns timeout errors for slow responses
- Returns connection errors for unreachable sites`,
    inputSchema: FetchUrlInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params: FetchUrlInput) => {
    try {
      // Fetch the URL content
      const response = await axios({
        method: "GET",
        url: params.url,
        timeout: 30000,
        headers: {
          "User-Agent": "MCP-Web-Search-Server/1.0.0",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
      });

      const contentType = response.headers['content-type'] || '';

      if (!contentType.includes('text/html') && !contentType.includes('text/plain')) {
        return {
          content: [{
            type: "text",
            text: `Error: Unsupported content type: ${contentType}. Only HTML and plain text are supported.`
          }]
        };
      }

      const content = response.data as string;

      let title = "";
      let extractedContent = content;
      let isExtracted = false;

      if (params.extract_text && contentType.includes('text/html')) {
        try {
          const $ = cheerio.load(content);
          title = $('title').text() || "";
          extractedContent = extractMainText(content, params.max_length);
          isExtracted = true;
        } catch (error) {
          // Fall back to raw content if extraction fails
          extractedContent = content.substring(0, params.max_length);
          isExtracted = false;
        }
      } else if (params.extract_text) {
        // For plain text, just truncate
        extractedContent = content.substring(0, params.max_length);
        isExtracted = false;
      }

      // Prepare structured output
      const output = params.extract_text ? {
        url: params.url,
        title: title,
        content: extractedContent,
        content_length: extractedContent.length,
        extracted: isExtracted
      } : {
        url: params.url,
        content: extractedContent,
        content_length: extractedContent.length,
        extracted: false
      };

      // Format text representation based on requested format
      let textContent: string;
      if (params.response_format === ResponseFormat.MARKDOWN) {
        if (params.extract_text && title) {
          textContent = `# ${title}\n\n**URL**: ${params.url}\n\n${extractedContent}`;
        } else {
          textContent = `# Content from ${params.url}\n\n${extractedContent}`;
        }
      } else {
        textContent = JSON.stringify(output, null, 2);
      }

      // Apply character limit
      textContent = truncateResponse(textContent);

      return {
        content: [{ type: "text", text: textContent }],
        structuredContent: output
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: handleApiError(error)
        }]
      };
    }
  }
);

// Main function for stdio transport
async function runServer() {
  // Check if search API credentials are available (warn if missing)
  if (!process.env.GOOGLE_SEARCH_API_KEY || !process.env.GOOGLE_SEARCH_ENGINE_ID) {
    console.error("WARNING: GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables are required for web search functionality.");
    console.error("URL content fetching will still work without these credentials.");
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Web Search MCP server running via stdio");
}

// Handle graceful shutdown
process.on("SIGINT", async () => {
  console.error("\nShutting down Web Search MCP server...");
  process.exit(0);
});

process.on("SIGTERM", async () => {
  console.error("\nShutting down Web Search MCP server...");
  process.exit(0);
});

// Start the server
runServer().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});