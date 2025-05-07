# Elections Canada MCP Server

This is a Model Context Protocol (MCP) server that provides access to Canadian federal election data. It currently supports results from the 2021 election, redistributed to the 2023 riding boundaries. Future updates will include past elections, census demographics, and real-time projections.

Brought to you by [ThreeFortyThree](https://threefortythree.ca), this server powers [ThreeFortyThree Chat](https://threefortythree.ca/chat) and is available for use with local models via Claude Desktop.

---

## 🛠 Setup

### Installation (via PyPI)

```bash
uv pip install elections-canada-mcp-server
```

To install development dependencies:

```bash
uv pip install 'elections-canada-mcp-server[dev]'
```

---

### Usage with Claude Desktop

1. Make sure the server is installed:

```bash
uv pip install elections-canada-mcp-server
```

2. Open your `claude_desktop_config.json` and add the following block:

```json
{
  "elections_canada_data": {
    "command": "uv",
    "args": ["run", "elections-canada-mcp"]
  }
}
```

3. Restart Claude Desktop.

4. Now you can ask Claude questions like:
   - "What were the 2021 election results in Toronto Centre?"
   - "Which ridings were closest for the NDP?"
   - "Show me the highest-margin wins for the Conservatives in 2021."

---

### Local Development

To test the server using MCP Inspector:

```bash
mcp dev elections_canada_mcp_server/server.py
```

This opens a web UI to test the server locally.

---

## 🧰 Tools

| Tool | Description | Input | Returns |
|------|-------------|-------|---------|
| `search_ridings` | Search ridings by name (accent-insensitive) | `search_term: str` | List of matching ridings |
| `get_party_votes` | Get vote share in a riding (optionally by party) | `riding_code: str, party_code: str (optional)` | Votes and percentage |
| `get_winning_party` | Get the winning party in a riding | `riding_code: str` | Winning party |
| `summarize_province_results` | Province-wide summary of votes/seats | `province_name_or_code: str` | Party results |
| `summarize_national_results` | Canada-wide election summary | — | National party results |
| `find_closest_ridings` | Find most competitive ridings | `num_results: int, party: str (optional)` | Closest margins |
| `best_and_worst_results` | Best/worst ridings for a party | `party: str, num_entries: int` | 4-category performance summary |

---

## 📚 Resources

| Resource | URI |
|----------|-----|
| All ridings | `elections-canada://ridings` |
| Single riding | `elections-canada://riding/{riding_code}` |
| Province | `elections-canada://province/{province_code}` |

---

## 📌 Province Codes

AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT

## 📌 Party Codes

LPC, CPC, NDP, BQ, GPC, PPC

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

© ThreeFortyThree Canada – [threefortythree.ca](https://threefortythree.ca)
