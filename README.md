# mcp-server-databe

An [MCP](https://modelcontextprotocol.io/) server for the [data.be](https://data.be) Belgian company information API.

## Tools

| Tool | Description |
|---|---|
| `company_info` | Detailed company information by VAT number |
| `financial_statements` | Annual reports with financial metrics |
| `legal_representative_persons` | Legal representative persons |
| `legal_representative_companies` | Legal representative companies |
| `bank_accounts` | Bank accounts for a company |
| `bank_account_check` | Check if an IBAN belongs to a company |
| `bank_account_lookup` | Find which company owns an IBAN |
| `stakeholders` | Stakeholders from annual reports |
| `vat_check` | Validate any European VAT number via VIES |
| `company_guess` | Quick company lookup by name/identifier |
| `company_search` | Advanced search with filters (NACE codes, zip, juridical form, etc.) |

## Setup

### 1. Get an API key

Request one at [data.be/en/api](https://data.be/en/api).

### 2. Set the environment variable

```sh
export DATABE_API_KEY="your-api-key"
```

### 3. Configure your MCP client

#### Claude Code

```sh
claude mcp add databe -- env DATABE_API_KEY=your-key-here uvx mcp-server-databe
```

#### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "databe": {
      "command": "uvx",
      "args": ["mcp-server-databe"],
      "env": {
        "DATABE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Local development

```sh
git clone https://github.com/bbbart/mcp-server-databe.git
cd mcp-server-databe
uv run mcp-server-databe
```

## License

MIT
