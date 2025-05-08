# DuckDB LLM UDF

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![DuckDB 0.8.0+](https://img.shields.io/badge/DuckDB-0.8.0+-yellow.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> Query your database in plain English—no SQL required. DuckDB LLM UDF translates natural language to SQL using large language models like OpenAI GPT-4 and Anthropic Claude.

## ✨ Overview

<p align="center">
  <img src="https://i.imgur.com/waxVImv.png" alt="Divider" width="600">
</p>

DuckDB LLM UDF bridges the gap between natural language and database queries. It's perfect for:

- **Data analysts** who need quick answers without writing complex SQL
- **Application developers** looking to add natural language query capabilities
- **SQL learners** who want to see how their questions translate to SQL
- **DuckDB users** who want to leverage the power of modern LLMs

This Python-based extension creates User-Defined Functions (UDFs) that let you query your database in plain English:

1. 📚 **Schema Analysis**: Automatically extracts your database schema metadata
2. 🤖 **LLM Integration**: Sends properly formatted prompts to OpenAI or Anthropic
3. 🔍 **SQL Generation**: Converts natural language to accurate SQL
4. ✅ **Safety First**: Asks for confirmation before executing any generated SQL
5. 📊 **Results Delivery**: Returns query results in standard DuckDB format

## 🚀 Installation

```bash
pip install duckdb_llm_udf
```

Or install from source:

```bash
git clone https://github.com/yourusername/duckdb_llm_udf.git
cd duckdb_llm_udf
pip install -e .
```

### Dependencies

The package will automatically install the required dependencies:

- **DuckDB** ≥ 0.8.0
- **python-dotenv** ≥ 0.19.0 (for .env file support)

Optional dependencies based on your chosen LLM provider:

- **OpenAI** (default): `pip install openai>=1.0.0`
- **Anthropic**: `pip install anthropic>=0.5.0`

## 🔍 Usage

### Python API

```python
import duckdb
from duckdb_llm_udf import register_llm_functions

# Connect to a database
conn = duckdb.connect('your_database.db')

# Register the LLM functions
register_llm_functions(conn)

# Set your API key (if not using environment variables)
conn.execute("SELECT llm_configure('api_key', 'your-api-key')")

# Ask a question in natural language
query = "Show me the top 5 customers by total order amount"

# Option 1: Generate SQL without executing (for review)
sql = conn.execute(f"SELECT ask_llm('{query}', 'execute', 'false')").fetchone()[0]
print(f"Generated SQL:\n{sql}")

# Option 2: Execute directly with user confirmation
result = conn.execute(f"SELECT ask_llm('{query}')").fetchall()
print(result)

# Direct Python function usage
from duckdb_llm_udf.llm_udf import ask_llm

# Generate SQL without executing
sql = ask_llm(query, conn, execute=False)
print(f"Generated SQL:\n{sql}")

# Execute with confirmation
results = ask_llm(query, conn)
print(results)
```

### SQL Interface

```sql
-- After installing and loading the extension
INSTALL 'duckdb_llm_udf';
LOAD 'duckdb_llm_udf';

-- Configure the extension (if not using environment variables)
SELECT llm_configure('api_key', 'your-api-key');
SELECT llm_configure('provider', 'openai');
SELECT llm_configure('model', 'gpt-4o');

-- Generate SQL without executing (for review)
SELECT ask_llm('Show me the top 5 customers by revenue', 'execute', 'false');

-- Execute with user confirmation
SELECT ask_llm('Show me the top 5 customers by revenue');
```

## ⚙️ Configuration

You can configure DuckDB LLM UDF in three ways:

### 1. Environment Variables

```bash
# API Keys (required for corresponding provider)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Configuration (all optional)
LLM_PROVIDER=openai        # Default: "openai", Alternatives: "anthropic"
LLM_MODEL=gpt-4o           # Default: "gpt-3.5-turbo" or "claude-3-sonnet-20240229"
LLM_TEMPERATURE=0.7        # Controls randomness (0.0-1.0)
LLM_MAX_TOKENS=4096        # Maximum tokens for LLM response
```

### 2. .env File (recommended for security)

Create a `.env` file in your project with the same variables as above:

```bash
# API Keys
OPENAI_API_KEY=sk-your-openai-key-here

# Configuration 
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.3
```

Variables will automatically load when the package is imported. See `examples/.env.example` for a template.

### 3. Runtime Configuration

SQL interface:
```sql
SELECT llm_configure('api_key', 'your-api-key');
SELECT llm_configure('provider', 'anthropic');
SELECT llm_configure('model', 'claude-3-opus-20240229');
SELECT llm_configure('temperature', '0.5');
SELECT llm_configure('max_tokens', '2048');
```

Python interface:
```python
conn.execute("SELECT llm_configure('api_key', 'your-api-key')")
conn.execute("SELECT llm_configure('model', 'gpt-4-turbo')")
```

## 🧪 Examples

The `examples/` directory contains ready-to-use examples:

- `basic_usage.py` - Core functionality demonstration
- `dotenv_usage.py` - Using environment variables with a .env file
- `sql_example.sql` - SQL interface usage
- `test_extraction.py` - Test schema extraction without LLM API calls

### Example Questions

Here are some example questions you can ask your database:

- "Show me the top 5 customers by total order amount"
- "How many orders were placed in each month of 2023?"
- "What's the average order value by product category?"
- "Find customers who haven't made a purchase in the last 30 days"
- "What product has generated the most revenue?"

## 🔧 How It Works

<p align="center">
  <img src="https://i.imgur.com/waxVImv.png" alt="Divider" width="600">
</p>

1. **Schema Analysis**: When you call `ask_llm()`, the function extracts your database schema metadata (tables, columns, types, foreign keys, etc.)

2. **Prompt Engineering**: Your natural language question is combined with the schema into a carefully crafted prompt that helps the LLM understand the context

3. **LLM Query**: The prompt is sent to the configured LLM (OpenAI or Anthropic) with instructions to generate valid SQL

4. **SQL Generation**: The LLM produces SQL based on your schema and question

5. **Safety Check**: The generated SQL is presented to you for review and confirmation

6. **Execution**: If approved, the SQL is executed and the results are returned in standard DuckDB format

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

Contributions are welcome and appreciated! Here's how you can help:

- 🐛 **Report bugs** by opening an issue
- 💡 **Suggest features** or improvements
- 🧪 **Improve tests** or add new test cases
- 📚 **Improve documentation** to make it clearer or more complete
- 🧑‍💻 **Submit pull requests** with bug fixes or new features

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 🙏 Credits

This project was built with:

- [DuckDB](https://duckdb.org/) - The in-process SQL OLAP database management system
- [OpenAI API](https://openai.com/api/) - For GPT model integration
- [Anthropic API](https://anthropic.com/) - For Claude model integration

## 📨 Contact

If you have any questions or need help, please open an issue on GitHub.
