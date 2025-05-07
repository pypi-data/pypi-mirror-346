AvalAgent
A Python client for interacting with AI models via the AvalAI OpenAI-compatible API, featuring automatic retries, model fallback, and robust error handling.

Features
🚀 Multi-model support: Works with GPT-4o, DeepSeek, Claude-3, and other AvalAI-supported models

🔄 Automatic retries & fallback: Falls back to secondary models if primary fails

🔒 Secure API key handling: Uses SecretStr for API key protection

📝 Built-in logging: Detailed logging for debugging and monitoring

⚡ LangChain integration: Compatible with LangChain's message formats

Installation
bash
pip install avalAgent
Usage
Basic Usage
python
from avalAgent import AvalAgent
from pydantic import SecretStr

# Initialize with your AvalAI API key
agent = AvalAgent(api_key=SecretStr("your-api-key-here"))

# Get a response
response = agent.get_response(
    system_prompt="You are a helpful assistant.",
    query="Explain quantum computing in simple terms"
)

print(response)
Advanced Configuration
python
agent = AvalAgent(
    api_key=SecretStr("your-api-key-here"),
    base_url="https://api.avalai.ir/v1",  # Default
    model_priority_list=[
        "gpt-4o",
        "deepseek-chat",
        "anthropic.claude-3-5-sonnet-20241022-v2:0"
    ],
    stop_after_attempt=3  # Max retry attempts
)

response = agent.get_response(
    system_prompt="You are a technical expert.",
    query="Explain neural networks",
    model="gpt-4o",  # Optional override
    temperature=0.3  # Control creativity
)
Model Support
AvalAgent supports all models available through the AvalAI API, including:

gpt-4o

deepseek-chat

anthropic.claude-3-5-sonnet-20241022-v2:0

And other OpenAI-compatible models

Error Handling
The agent automatically:

Retries failed requests (up to 3 times by default)

Falls back to secondary models if primary fails

Handles rate limits and network errors gracefully

License
This project is licensed under the MIT License - see the LICENSE file for details.