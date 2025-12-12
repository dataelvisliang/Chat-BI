# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-12-11

### Added
- **Flexible Expression Evaluator**: Implemented tokenizer-based parser in `utils/renderers.py` that can evaluate ANY pandas expression ending with `.tolist()`, `.values.tolist()`, or `.index.tolist()`
  - Supports complex nested operations (date parsing, filtering, groupby, aggregations)
  - Properly handles nested parentheses, brackets, and string literals
  - Works with expressions like: `df[pd.to_datetime(...).dt.period() == ...].groupby().count().index.tolist()`

- **Smart Chart Selection Logic**: Added 5-step decision tree to both ECharts and Plotly prompts
  - Step 1: Identify data types (temporal, categorical, numeric)
  - Step 2: Match keywords in user request
  - Step 3: Smart defaults for ambiguous requests
  - Step 4: Data-driven decisions (column cardinality, date detection)
  - Step 5: Critical data aggregation guidance

- **Data Aggregation Support**: Enhanced prompts to instruct LLM on proper data aggregation
  - Added WRONG vs CORRECT examples showing duplicate categories vs aggregated data
  - Common aggregation patterns (sum, count, average, max by category)
  - Automatic groupby for "by category" requests

- **Plotly Date Handling**: Comprehensive date/time support for Plotly charts
  - Automatic date parsing with `pd.to_datetime(errors='coerce', dayfirst=True)`
  - Chronological sorting using `.assign()` with temporary datetime column
  - ISO format conversion with `.dt.strftime("%Y-%m-%d")`
  - Date axis type configuration (`"xaxis": {"type": "date"}`)

- **Error Display**: Added problematic spec display to Plotly tab (matching ECharts behavior)

### Changed
- **Default Model**: Changed from `nvidia/nemotron-nano-12b-v2-vl:free` to `amazon/nova-2-lite-v1:free` in app.py

- **ECharts Prompt Enhancements**:
  - Expanded from basic prompt to comprehensive 104-line system prompt
  - Added support for 13+ chart types (line, bar, scatter, pie, boxplot, heatmap, treemap, sunburst, gauge, funnel, radar, candlestick, graph)
  - Added chart selection keywords and data-driven logic
  - Emphasized unquoted df syntax and aggregation requirements

- **Plotly Prompt Enhancements**:
  - Expanded from basic prompt to comprehensive 153-line system prompt
  - Added support for 8+ chart types (line, bar, scatter, pie, box, heatmap, funnel, 3D)
  - Added date sorting and formatting instructions
  - Emphasized unquoted df syntax and aggregation requirements
  - Added special handling for international date formats

### Fixed
- **Regex Pattern Limitations**: Replaced simple regex patterns with tokenizer-based approach
  - Old: Only matched `df["column"].tolist()` and basic `df.groupby()`
  - New: Handles arbitrarily complex pandas expressions with nested calls

- **Data Aggregation Bug**: Fixed duplicate categories in charts
  - Problem: Charts showed "Type A, Type A, Type B" instead of "Type A, Type B"
  - Solution: Added aggregation guidance with groupby examples to prompts

- **Plotly Date Ordering**: Fixed chronological ordering of dates
  - Problem: Dates displayed in data order or alphabetically, not chronologically
  - Solution: Sort by parsed datetime using `.assign(_temp_date=...).sort_values()`
  - Added international date format support with `dayfirst=True`

- **Empty Chart Specs**: Fixed LLM generating empty arrays `[]`
  - Added multiple CRITICAL warnings emphasizing use of `df["column"].tolist()`
  - Added examples showing WRONG vs CORRECT patterns

### Technical Details

#### Expression Evaluator Architecture
Location: `utils/renderers.py`

**Key Components**:
1. `scan_for_tolist_end()`: Tokenizer that tracks parentheses/bracket depth
2. Regex pattern `\b(df|pd)[\[\.\(]` to find expression starts
3. Skip logic to avoid reprocessing nested df/pd references
4. Graceful error handling with fallback to original expression

**Supported Expression Patterns**:
- Simple: `df["Column"].tolist()`
- GroupBy: `df.groupby("Category")["Value"].sum().values.tolist()`
- Filtering: `df[df["Amount"] > 100]["Name"].tolist()`
- Date Operations: `pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d").tolist()`
- Complex Nested: `df[pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.to_period("M") == pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.to_period("M").max()].groupby("Category")["Sales"].sum().index.tolist()`

#### Plotly Date Sorting Pattern
```python
# WRONG (unsorted)
"x": pd.to_datetime(df["Order Date"]).dt.strftime("%Y-%m-%d").tolist()

# CORRECT (sorted chronologically)
"x": df.assign(_temp_date=pd.to_datetime(df["Order Date"], errors='coerce', dayfirst=True))
      .sort_values("_temp_date")["_temp_date"]
      .dt.strftime("%Y-%m-%d").tolist()
```

### Files Modified

**Core Functionality**:
- `utils/renderers.py`: Complete rewrite of expression evaluation (72 lines → 126 lines)

**Prompts**:
- `prompts/echarts_prompt.py`: Enhanced from 32 lines → 104 lines
- `prompts/plotly_prompt.py`: Enhanced from 32 lines → 153 lines

**UI**:
- `app.py`: Changed default model
- `tabs/plotly_tab.py`: Added problematic spec display

**Structure**:
- No changes to `tabs/echarts_tab.py` (already had error display)
- No changes to `tabs/pygwalker_tab.py`

### Testing
All features tested and verified:
- ✅ Complex nested pandas expressions with date parsing
- ✅ GroupBy aggregations with sum/count/mean
- ✅ Date sorting in chronological order (Plotly)
- ✅ International date format support (dd/mm/yyyy)
- ✅ Backward compatibility with simple expressions
- ✅ Error handling for malformed expressions
- ✅ Skip logic for nested df/pd references

### Notes
- Expression evaluator uses `eval()` with restricted scope (`{"df": df, "pd": pd}`) for security
- All prompts emphasize generating unquoted expressions to ensure proper evaluation
- Date handling includes `errors='coerce'` to gracefully handle invalid dates
- Both ECharts and Plotly tabs now have feature parity for complex expressions
