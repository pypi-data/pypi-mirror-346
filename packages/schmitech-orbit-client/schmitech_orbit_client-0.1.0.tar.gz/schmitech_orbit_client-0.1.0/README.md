# Schmitech Orbit Client

A Python client for interacting with Orbit chat servers. This client provides a command-line interface for chatting with Orbit servers, supporting both standard and MCP protocol formats.

## Installation

```bash
pip install schmitech-orbit-client
```

## Usage

After installation, you can use the client in two ways:

### 1. Command-line Interface

The simplest way to use the client is through the command-line interface:

```bash
# Basic usage with default settings
orbit-chat --url http://your-server:3000

# Advanced usage with all options
orbit-chat --url http://your-server:3000 \
           --api-key your-api-key \
           --debug \
           --show-timing \
           --mcp
```

#### Command-line Options

- `--url`: Chat server URL (default: http://localhost:3000)
- `--api-key`: API key for authentication
- `--debug`: Enable debug mode to see request/response details
- `--show-timing`: Show latency timing information
- `--mcp`: Use MCP protocol format instead of standard format

#### Interactive Features

- Use up/down arrow keys to navigate through chat history
- Type `exit` or `quit` to end the conversation
- Press Ctrl+C to interrupt the current response
- Chat history is saved in `~/.orbit_client_history/chat_history`

### 2. Python Module

You can also use the client in your Python code:

```python
from schmitech_orbit_client import stream_chat

# Basic usage
response, timing_info = stream_chat(
    url="http://your-server:3000",
    message="Hello, how are you?"
)

# Advanced usage with all options
response, timing_info = stream_chat(
    url="http://your-server:3000",
    message="Hello, how are you?",
    api_key="your-api-key",  # optional
    debug=True,              # optional
    use_mcp=True            # optional
)

# The response contains:
# - response: The full text response from the server
# - timing_info: Dictionary with timing metrics
#   - total_time: Total request time
#   - time_to_first_token: Time until first response token
```

## Features

- **Interactive CLI**: Command-line interface with history navigation
- **Protocol Support**: Both standard and MCP protocol formats
- **Real-time Streaming**: Responses appear gradually, character by character
- **Colored Output**: Better readability with syntax highlighting
- **Debug Mode**: Detailed request/response information for troubleshooting
- **Performance Metrics**: Latency timing information
- **Authentication**: API key support for secure communication
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Unicode Support**: Full support for non-English characters

## Examples

### Basic Chat Session
```bash
$ orbit-chat --url http://localhost:3000
Welcome to the Orbit Chat Client!
Server URL: http://localhost:3000
Type 'exit' or 'quit' to end the conversation.
You can use arrow keys to navigate, up/down for history.

You: Hello, how are you?
Assistant: I'm doing well, thank you for asking! How can I help you today?

You: exit
Goodbye!
```

### Debug Mode
```bash
$ orbit-chat --url http://localhost:3000 --debug
Debug - Request:
{
  "message": "Hello",
  "stream": true
}
Debug - Received:
{
  "text": "Hi there!"
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 