# 🤖 MCP Multi-Agent Chat System

A complete Model Context Protocol (MCP) implementation featuring multiple specialized AI agents with a beautiful Streamlit chat interface. This system demonstrates how to build scalable, modular AI applications using MCP architecture.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Usage Guide](#usage-guide)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)

## 🎯 Overview

This project implements a multi-agent AI system using the Model Context Protocol (MCP) with the following components:

### **Core Features**
- **🧮 Calculator Agent** - Specialized in mathematical operations
- **🌤️ Weather Agent** - Provides weather information and forecasts
- **🤖 Streamlit Chat UI** - Modern web interface for interaction
- **🔄 Intelligent Routing** - Auto-detects which agent to use
- **📊 Real-time Chat** - Full conversation history and context

### **What You'll Learn**
- How to build MCP servers with FastMCP
- Multi-agent system architecture
- LangChain agent integration
- Streamlit web application development
- Windows-compatible async operations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Chat UI                            │
│                    (mcp_chat_manual.py)                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MultiServerMCPClient                        │
│                    (LangChain MCP Adapters)                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│   Calculator MCP    │ │   Weather MCP       │ │   LangChain Agents  │
│   Server            │ │   Server            │ │   (OpenAI Functions)│
│   (Port 8001)       │ │   (Port 8002)       │ │                     │
│                     │ │                     │ │                     │
│ • add_numbers       │ │ • get_weather       │ │ • Agent Executors   │
│ • subtract_numbers  │ │ • get_forecast      │ │ • Prompt Templates  │
│ • multiply_numbers  │ │ • temp_conversion   │ │ • Tool Integration  │
│ • divide_numbers    │ │ • weather_alerts    │ │ • Tool Integration  │
│ • calculate_power   │ │                     │ │ • Tool Integration  │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

### **Technology Stack**
- **FastMCP** - MCP server framework
- **LangChain** - Agent orchestration
- **Streamlit** - Web interface
- **OpenAI GPT-4o** - Language model
- **HTTP Transport** - Cross-platform compatibility

## 📋 Prerequisites

### **System Requirements**
- Python 3.8 or higher
- Windows 10/11, macOS, or Linux
- 4GB RAM minimum
- Internet connection for OpenAI API

### **Software Dependencies**
- Python 3.8+
- pip (Python package manager)
- Git (for cloning the repository)

### **API Keys Required**
- OpenAI API key (for GPT-4o model)

## 🚀 Installation

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd MCPServer
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Environment Configuration**
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

**How to get OpenAI API key:**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy and paste it in your `.env` file

## ⚡ Quick Start

### **Option 1: Manual Server Startup (Recommended)**

#### **Terminal 1: Start Calculator Server**
```bash
python calculator_server.py
```
**Expected Output:**
```
🚀 Starting Calculator MCP Server on http://localhost:8001
```

#### **Terminal 2: Start Weather Server**
```bash
python weather_server.py
```
**Expected Output:**
```
🌤️ Starting Weather MCP Server on http://localhost:8002
```

#### **Terminal 3: Start Chat Interface**
```bash
streamlit run mcp_chat_manual.py
```
**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

### **Option 2: Auto Server Startup (Advanced)**
```bash
streamlit run mcp_chat_ui.py
```
*Note: May have issues on Windows due to subprocess limitations*

## 📖 Detailed Setup

### **Understanding the Components**

#### **1. MCP Servers**
MCP servers are standalone processes that provide tools to AI agents:

**Calculator Server (`calculator_server.py`)**
- **Port:** 8001
- **Purpose:** Mathematical operations
- **Tools:** 5 mathematical functions
- **Transport:** HTTP (streamable-http)

**Weather Server (`weather_server.py`)**
- **Port:** 8002
- **Purpose:** Weather information
- **Tools:** 4 weather-related functions
- **Transport:** HTTP (streamable-http)

#### **2. Chat Interface (`mcp_chat_manual.py`)**
- **Framework:** Streamlit
- **Purpose:** Web-based chat interface
- **Features:** Agent selection, auto-detection, chat history
- **Port:** 8501 (default Streamlit port)

#### **3. Agent System**
- **Framework:** LangChain
- **Model:** OpenAI GPT-4o
- **Agent Type:** OpenAI Functions Agent
- **Features:** Tool integration, conversation memory

### **File Structure**
```
MCPServer/
├── calculator_server.py      # Calculator MCP server
├── weather_server.py         # Weather MCP server
├── mcp_chat_manual.py        # Main chat interface (recommended)
├── mcp_chat_ui.py           # Auto-startup chat interface
├── simple_direct.py         # Direct tools (no MCP)
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .env                    # Environment variables (create this)
```

## 🎮 Usage Guide

### **Starting the System**

#### **Step-by-Step Process**

1. **Open three terminal windows/command prompts**

2. **Terminal 1 - Calculator Server:**
   ```bash
   cd MCPServer
   python calculator_server.py
   ```
   - Keep this terminal open
   - You should see the server start message

3. **Terminal 2 - Weather Server:**
   ```bash
   cd MCPServer
   python weather_server.py
   ```
   - Keep this terminal open
   - You should see the server start message

4. **Terminal 3 - Chat Interface:**
   ```bash
   cd MCPServer
   streamlit run mcp_chat_manual.py
   ```
   - This will open your web browser
   - The interface will automatically connect to both servers

### **Using the Chat Interface**

#### **Agent Selection Options**

1. **Auto-Detect (Recommended)**
   - The system automatically chooses the appropriate agent
   - Based on keyword analysis of your query

2. **Manual Selection**
   - Choose "Calculator Agent" for math queries
   - Choose "Weather Agent" for weather queries

#### **Example Conversations**

**Calculator Queries:**
```
User: "What is 15 + 27?"
Agent: [🧮 Calculator] I'll calculate that for you. 15 + 27 = 42

User: "Calculate 5 to the power of 3"
Agent: [🧮 Calculator] 5 raised to the power of 3 equals 125

User: "Multiply 8 and 12"
Agent: [🧮 Calculator] 8 multiplied by 12 equals 96
```

**Weather Queries:**
```
User: "What's the weather in Tokyo?"
Agent: [🌤️ Weather] ☁️ Cloudy, 68°F (20°C), Humidity: 70%, Wind: 5 mph

User: "Get 3-day forecast for London"
Agent: [🌤️ Weather] Weather forecast for London:
  🌧️ Day 1: Rain, 55°F | 🌙 Night: Heavy Rain, 48°F
  ⛅ Day 2: Partly Cloudy, 58°F | 🌙 Night: Clear, 50°F
  🌤️ Day 3: Sunny, 62°F | 🌙 Night: Clear, 53°F

User: "Convert 25°C to Fahrenheit"
Agent: [🌤️ Weather] 25°C = 77.0°F
```

### **Advanced Features**

#### **Chat History**
- All conversations are saved in the session
- Use "Clear Chat" to start fresh
- Chat history is maintained until page refresh

#### **Debug Information**
- Enable "Show Debug Info" in sidebar
- View agent status, tool count, and system information
- Helpful for troubleshooting

#### **Reinitialize Agents**
- Use if servers restart or connection issues occur
- Reconnects to MCP servers and reloads tools

## 🔧 API Reference

### **Calculator Server Tools**

| Tool | Description | Parameters | Example |
|------|-------------|------------|---------|
| `add_numbers` | Add two numbers | `a: int, b: int` | `add_numbers(5, 3)` |
| `subtract_numbers` | Subtract second from first | `a: int, b: int` | `subtract_numbers(10, 4)` |
| `multiply_numbers` | Multiply two numbers | `a: int, b: int` | `multiply_numbers(6, 7)` |
| `divide_numbers` | Divide first by second | `a: int, b: int` | `divide_numbers(20, 5)` |
| `calculate_power` | Base to the power of exponent | `base: int, exponent: int` | `calculate_power(2, 8)` |

### **Weather Server Tools**

| Tool | Description | Parameters | Example |
|------|-------------|------------|---------|
| `get_weather` | Current weather for city | `city: str` | `get_weather("Tokyo")` |
| `get_weather_forecast` | Multi-day forecast | `city: str, days: int` | `get_forecast("London", 3)` |
| `get_temperature_conversion` | Celsius to Fahrenheit | `celsius: float` | `temp_conversion(25.0)` |
| `get_weather_alerts` | Weather alerts for city | `city: str` | `weather_alerts("New York")` |

### **Available Cities**
- New York, London, Tokyo, Sydney, Paris
- Berlin, Moscow, Dubai, Singapore, Mumbai

## 🛠️ Troubleshooting

### **Common Issues and Solutions**

#### **1. "Failed to initialize agent" Error**

**Symptoms:**
- Error message appears when starting the chat interface
- Agents show as not initialized

**Solutions:**
1. **Check server status:**
   ```bash
   # Check if ports are in use
   netstat -an | findstr :8001
   netstat -an | findstr :8002
   ```

2. **Restart servers:**
   - Stop all servers (Ctrl+C)
   - Start them again in order

3. **Check firewall:**
   - Ensure ports 8001 and 8002 are not blocked
   - Temporarily disable firewall for testing

#### **2. "Timeout connecting to server" Error**

**Symptoms:**
- Timeout errors when loading tools
- Servers appear to be running but connection fails

**Solutions:**
1. **Wait longer:**
   - Servers need 3-5 seconds to fully start
   - Try refreshing the page after 10 seconds

2. **Check server output:**
   - Look for error messages in server terminals
   - Ensure servers show "Starting... on http://localhost:800X"

3. **Port conflicts:**
   ```bash
   # Kill processes using the ports
   netstat -ano | findstr :8001
   taskkill /PID <PID> /F
   ```

#### **3. "NotImplementedError" on Windows**

**Symptoms:**
- Asyncio subprocess errors
- Server startup failures

**Solutions:**
1. **Use manual startup:**
   - Use `mcp_chat_manual.py` instead of `mcp_chat_ui.py`
   - Start servers manually in separate terminals

2. **Check Python version:**
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

3. **Reinstall dependencies:**
   ```bash
   pip uninstall fastmcp langchain-mcp-adapters
   pip install fastmcp langchain-mcp-adapters
   ```

#### **4. OpenAI API Errors**

**Symptoms:**
- "Invalid API key" errors
- Rate limiting messages

**Solutions:**
1. **Check API key:**
   - Verify `.env` file exists and contains valid key
   - Ensure no extra spaces or characters

2. **Check API quota:**
   - Visit OpenAI dashboard to check usage
   - Ensure account has sufficient credits

3. **Test API key:**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        https://api.openai.com/v1/models
   ```

### **Debug Mode**

Enable debug information in the sidebar:
1. Check "Show Debug Info" in the sidebar
2. View agent status, tool counts, and system info
3. Use this information when reporting issues

### **Log Files**

For advanced debugging, check:
- Server terminal output for MCP server logs
- Streamlit logs in the terminal where you ran `streamlit run`
- Browser developer console for frontend errors

## 🔄 Development

### **Adding New Tools**

#### **To Calculator Server:**
1. Open `calculator_server.py`
2. Add new function with `@mcp.tool()` decorator:
   ```python
   @mcp.tool()
   def new_calculation(param1: int, param2: int) -> int:
       """Description of what this tool does"""
       return result
   ```
3. Restart the calculator server

#### **To Weather Server:**
1. Open `weather_server.py`
2. Add new function with `@mcp.tool()` decorator
3. Restart the weather server

### **Creating New Agents**

1. **Create new MCP server:**
   ```python
   from fastmcp import FastMCP
   
   mcp = FastMCP("NewAgentServer")
   
   @mcp.tool()
   def new_tool(param: str) -> str:
       return "result"
   
   if __name__ == "__main__":
       mcp.run(transport="streamable-http", host="127.0.0.1", port=8003)
   ```

2. **Add to chat interface:**
   - Add new client in `initialize_agents()`
   - Create new agent with appropriate prompt
   - Add to agent selection logic

### **Customizing Prompts**

Modify agent prompts in the chat interface:
```python
calc_prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system prompt here"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
```

### **Environment Variables**

Additional environment variables you can use:
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL_NAME=gpt-4o
STREAMLIT_SERVER_PORT=8501
CALCULATOR_SERVER_PORT=8001
WEATHER_SERVER_PORT=8002
```

## 🤝 Contributing

### **How to Contribute**

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Make your changes**
4. **Test thoroughly:**
   - Test on Windows, macOS, and Linux
   - Ensure all agents work correctly
   - Check error handling
5. **Submit a pull request**

### **Development Setup**

1. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/MCPServer.git
   cd MCPServer
   ```

2. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8
   ```

3. **Run tests:**
   ```bash
   pytest tests/
   ```

### **Code Style**

- Use Black for code formatting
- Follow PEP 8 guidelines
- Add type hints to all functions
- Include docstrings for all public functions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastMCP** - For the excellent MCP server framework
- **LangChain** - For agent orchestration capabilities
- **Streamlit** - For the beautiful web interface
- **OpenAI** - For the GPT-4o language model

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Search existing issues** in the repository
3. **Create a new issue** with:
   - Detailed error message
   - Steps to reproduce
   - System information (OS, Python version)
   - Debug information from the interface

---

**Happy coding! 🚀**

This comprehensive system demonstrates the power of MCP architecture for building scalable, modular AI applications. Feel free to extend it with your own tools and agents! 