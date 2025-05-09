# Technical Indicator Analysis Tool
This tool provides mcp server for analyzing technical indicators of ETFs and stocks. It utilizes the `akshare` library to fetch historical data and calculates technical indicators such as RSI, Bollinger Bands, and moving averages. The tool supports both ETF and stock historical data analysis.

## API Documentation

Interfaces provided with mcp server:

### analyze_etf_technical

```python
@mcp.tool()
def analyze_etf_technical(etf_code='510300'):
    """
    ETF technical indicator analysis tool
    :param etf_code: ETF code (e.g. '510300')
    :return: Markdown table containing technical indicators (last 5 records)
    """
```

**Parameters**:
- `etf_code`: ETF code, defaults to '510300'(CSI 300 ETF)

**Returns**:
- Markdown table containing following technical indicators:
  - Price data
  - RSI indicator
  - Bollinger Bands
  - Moving averages

**Example**:
```python
result = analyze_etf_technical('510300')
print(result)
```

### analyze_stock_hist_technical

```python
@mcp.tool()
def analyze_stock_hist_technical(stock_code='000001'):
    """
    Stock historical data technical indicator analysis tool
    :param stock_code: Stock code (e.g. '000001')
    :return: Markdown table containing technical indicators (last 5 records)
    """
```

**Parameters**:
- `stock_code`: Stock code, defaults to '000001'(Ping An Bank)

**Returns**:
- Markdown table containing following technical indicators:
  - Price data
  - RSI indicator
  - Bollinger Bands
  - Moving averages

**Example**:
```python
result = analyze_stock_hist_technical('000001')
print(result)
```
## Installation
```bash
pip install technical-analysis-mcp
```

## MCP Configuration Example
```json
{
  "mcpServers": {
    "technical-analysis-mcp": {
      "command": "technical-analysis-mcp",
      "args": []
    }
  }
}
```
