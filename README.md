# Chat BI - AI-Powered Data Analysis

A Streamlit-based Chat BI application that combines conversational AI with interactive data visualization using PygWalker and Graphic Walker. Upload any CSV file and chat with your data!

## Features

- 📤 **CSV Upload**: Upload any CSV file to analyze
- 💬 **Chat Interface**: Ask questions about your data using natural language
- 📊 **AI-Generated Visualizations**: Automatic chart generation based on your requests
- 🔄 **Hybrid Interaction**: Chat-driven analysis + drag-and-drop chart building
- 🤖 **Multiple LLM Support**: Free models (NVIDIA) or premium (Claude, GPT-4) via OpenRouter
- 📈 **Interactive Charts**: Powered by Graphic Walker (Vega-Lite)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. **Get an OpenRouter API Key**
   - Sign up at [openrouter.ai](https://openrouter.ai)
   - Get your free API key

2. **Run the App**
   ```bash
   streamlit run app.py
   ```

3. **Upload Your Data**
   - Click "Browse files" and upload your CSV file
   - The app will automatically analyze the structure

4. **Configure (Optional)**
   - Enter your OpenRouter API key in the sidebar
   - Change the model if desired (default: nvidia/nemotron-nano-12b-v2-vl:free)

5. **Start Analyzing**
   - Ask questions in the chat
   - Request visualizations
   - Explore data with drag-and-drop charts

## Example Chat Commands

### General Questions
- "What columns are in this dataset?"
- "Show me summary statistics"
- "What patterns do you see in the data?"
- "Are there any outliers?"

### Visualization Requests (Examples)
- "Show me a bar chart of sales by category"
- "Create a scatter plot of price vs quantity"
- "Display a line chart of revenue over time"
- "Compare values across different groups"
- "Show the distribution of [column name]"

**Note:** The AI will adapt to your specific dataset and generate appropriate visualizations!

## How It Works

1. **Upload CSV**
   - App analyzes structure (numeric vs categorical columns)
   - Generates dataset summary

2. **Chat Interface** (Top Section)
   - Enter natural language queries
   - LLM analyzes your dataset context
   - Generates insights or Vega-Lite chart specifications

3. **Visualization Panel** (Bottom Section)
   - Displays Graphic Walker interface
   - Auto-loads AI-generated charts
   - Supports manual drag-and-drop editing
   - Full interactivity for data exploration

4. **AI Chart Generation**
   - LLM generates Vega-Lite specifications
   - Charts update in real-time
   - Modify AI charts or create custom ones

## Use Cases

- **Sales Analysis**: Analyze supermarket/retail data
- **Customer Analytics**: Explore user behavior patterns
- **Financial Data**: Visualize revenue, expenses, trends
- **Survey Results**: Understand questionnaire responses
- **Any CSV Data**: Works with any structured dataset!

## Technical Stack

- **Streamlit**: Web application framework
- **PygWalker**: Python binding for Graphic Walker
- **Graphic Walker**: Interactive data visualization component
- **OpenAI SDK**: For OpenRouter API integration
- **Pandas**: Data manipulation

## OpenRouter Integration

The app uses OpenRouter API to access multiple LLM providers through a single interface:

```python
client = OpenAI(
    api_key=api_key_input,
    base_url="https://openrouter.ai/api/v1"
)
```

Supported models:
- `anthropic/claude-3.5-sonnet` (recommended)
- `openai/gpt-4o`
- `google/gemini-pro-1.5`

## Advanced Features

### Spec Management
- View current chart specification in JSON format
- Clear specs to reset to default view
- Specs persist across chat interactions

### Manual Override
- Use Graphic Walker's drag-and-drop interface anytime
- Manually create and customize visualizations
- Save chart configurations

## License

This is a demonstration project for educational purposes.
