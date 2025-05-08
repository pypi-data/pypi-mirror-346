# mcp-paperless-ngx MCP Server

A MCP server that connects to Paperless-ngx DMS (Document Management System) and exposes its documents as resources. This server allows you to:

- View and access all your Paperless-ngx documents as resources
- Read document details including metadata
- Search documents using the Whoosh query language (Paperless-ngx's powerful search syntax)
- Generate summaries of your documents filtered by search criteria

## Components

### Resources

The server exposes Paperless-ngx documents as resources:
- Custom `paperless://` URI scheme for accessing individual documents
- Each document resource has a name, description, and appropriate MIME type
- Document metadata like creation date, tags, and correspondents is included

### Prompts

The server provides one prompt:
- `summarize-documents`: Creates summaries of Paperless-ngx documents
  - Optional "query" argument to filter which documents to summarize
  - Optional "style" argument to control detail level (brief/detailed)
  - Generates a prompt combining document metadata and content snippets

### Tools

The server implements one tool:
- `search-documents`: Searches for documents in Paperless-ngx using Whoosh query language
  - Takes "query" as required string argument using Whoosh query syntax
  - Returns a list of matching documents with metadata
  - Supports advanced search features including:
    - Field-specific searches (type:invoice, correspondent:university)
    - Date-based queries (created:[2020 to 2023], added:yesterday)
    - Logical operators (AND, OR, NOT)
    - Wildcards for inexact matching (electr*)

## Configuration

### Environment Variables

The server requires the following environment variables to be set:

- `PAPERLESS_NGX_URI`: The base URL of your Paperless-ngx instance (e.g., `https://paperless.example.com`)
- `PAPERLESS_NGX_TOKEN`: An API token for authenticating with Paperless-ngx

You can create a `.env` file in the project root with these variables:

```
PAPERLESS_NGX_URI=https://your-paperless-instance.com
PAPERLESS_NGX_TOKEN=your-api-token
```

### Creating an API Token

To create an API token for Paperless-ngx:

1. Log in to your Paperless-ngx instance
2. Go to Settings → Administration
3. Click on "API Tokens"
4. Create a new token with appropriate permissions
5. Copy the token value for the `PAPERLESS_NGX_TOKEN` environment variable

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  
  ```
  "mcpServers": {
    "mcp-paperless-ngx": {
      "command": "uvx",
      "args": [
        "mcp-paperless-ngx"
      ],
      "env": {
        "PAPERLESS_NGX_URI": "https://your-paperless-instance.com",
        "PAPERLESS_NGX_TOKEN": "your-api-token"
      }
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  
  ```
  "mcpServers": {
    "mcp-paperless-ngx": {
      "command": "uvx",
      "args": [
        "mcp-paperless-ngx"
      ],
      "env": {
        "PAPERLESS_NGX_URI": "https://your-paperless-instance.com",
        "PAPERLESS_NGX_TOKEN": "your-api-token"
      }
    }
  }
  ```
</details>

### Example Usage

Once the MCP server is properly configured, you can:

1. Access documents by asking Claude to list available documents
2. Search for specific documents using natural language or specific queries
3. Get detailed information about specific documents
4. Ask Claude to summarize documents matching certain criteria

Example prompts:
- "Show me a list of my Paperless-ngx documents"
- "Search for my documents using the query: type:invoice AND (created:[2023-01-01 to 2023-12-31])"
- "Find documents with Whoosh query: correspondent:university AND tag:important"
- "Search for documents with the query: insurance contract* AND NOT expired"
- "Summarize the content of my tax documents from 2023 using query: tag:tax created:[2023-01-01 to 2023-12-31]"

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

## Search Syntax Reference

Paperless-ngx uses the [Whoosh](https://whoosh.readthedocs.io/en/latest/querylang.html) query language for its search functionality. This section provides a quick reference for the most common search patterns.

### Basic Search

By default, Paperless returns documents that contain all words in your query:
```
invoice receipt
```
This matches documents containing both "invoice" AND "receipt".

### Field-Specific Searches

You can search within specific document fields:
```
type:invoice                 # Documents of type "invoice"
correspondent:university     # Documents from "university" correspondent
tag:important                # Documents with "important" tag
```

### Date-Based Searches

Search by document dates using various formats:
```
created:[2020 to 2023]       # Date range (created between 2020-2023)
added:yesterday              # Relative date (added yesterday)
modified:today               # Relative date (modified today)
```

### Logical Operators

Combine terms with logical operators:
```
invoice AND receipt          # Documents with both terms
invoice OR receipt           # Documents with either term
invoice AND NOT paid         # Documents with "invoice" but not "paid"
invoice AND (paid OR unpaid) # More complex expressions
```

### Inexact Matching

Search for variations of terms:
```
electr*                      # Wildcard search (matches "electric", "electronics", etc.)
```

For more details on Whoosh query syntax, see the [official documentation](https://whoosh.readthedocs.io/en/latest/querylang.html).

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv run mcp-paperless-ngx
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
