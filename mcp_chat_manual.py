# mcp_chat_manual.py
import streamlit as st
import asyncio
import os
import sys
import traceback
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

# Fix for Windows asyncio issues
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Load environment variables
load_dotenv()

def initialize_agents():
    """Initialize the MCP clients and agents"""
    try:
        st.info("Connecting to MCP servers...")
        
        # Initialize the MCP clients
        calc_client = MultiServerMCPClient({
            "calculator": {
                "url": "http://localhost:8001/mcp",
                "transport": "streamable_http",
            }
        })
        
        weather_client = MultiServerMCPClient({
            "weather": {
                "url": "http://localhost:8002/mcp",
                "transport": "streamable_http",
            }
        })
        
        st.info("MCP Clients created successfully")
        
        # Get tools from servers
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Load calculator tools
        try:
            calc_tools = loop.run_until_complete(asyncio.wait_for(calc_client.get_tools(), timeout=30))
            st.info(f"Calculator tools loaded: {len(calc_tools)} tools")
        except asyncio.TimeoutError:
            st.error("Timeout connecting to calculator server. Make sure it's running on http://localhost:8001")
            return None, None
        except Exception as e:
            st.error(f"Error loading calculator tools: {str(e)}")
            st.error("Make sure calculator server is running with: python calculator_server.py")
            return None, None
        
        # Load weather tools
        try:
            weather_tools = loop.run_until_complete(asyncio.wait_for(weather_client.get_tools(), timeout=30))
            st.info(f"Weather tools loaded: {len(weather_tools)} tools")
        except asyncio.TimeoutError:
            st.error("Timeout connecting to weather server. Make sure it's running on http://localhost:8002")
            return None, None
        except Exception as e:
            st.error(f"Error loading weather tools: {str(e)}")
            st.error("Make sure weather server is running with: python weather_server.py")
            return None, None
        
        # Create LLM
        llm = ChatOpenAI(model_name="gpt-4o")
        st.info("LLM created successfully")
        
        # Create calculator agent
        calc_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful calculator assistant. Use the available tools to perform mathematical calculations. Always use the appropriate tool for calculations."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        calc_agent = create_openai_functions_agent(llm, calc_tools, calc_prompt)
        calc_executor = AgentExecutor(agent=calc_agent, tools=calc_tools, verbose=True)
        
        # Create weather agent
        weather_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful weather assistant. Use the available tools to provide weather information. Always use the appropriate tool for weather queries."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        weather_agent = create_openai_functions_agent(llm, weather_tools, weather_prompt)
        weather_executor = AgentExecutor(agent=weather_agent, tools=weather_tools, verbose=True)
        
        st.info("Agents created successfully")
        
        return calc_executor, weather_executor
    except Exception as e:
        st.error(f"Failed to initialize agents: {str(e)}")
        st.error(f"Full error: {traceback.format_exc()}")
        return None, None

# Initialize session state
if "calc_agent" not in st.session_state:
    st.session_state.calc_agent, st.session_state.weather_agent = initialize_agents()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# UI
st.title("🤖 MCP Multi-Agent Chat (Manual)")
st.markdown("Chat with specialized agents: **🧮 Calculator** and **🌤️ Weather**")

# Setup instructions
st.sidebar.markdown("### Setup Instructions")
st.sidebar.markdown("""
1. Start calculator server:
   ```bash
   python calculator_server.py
   ```

2. Start weather server:
   ```bash
   python weather_server.py
   ```

3. Refresh this page
""")

# Agent selection
agent_type = st.sidebar.selectbox(
    "Choose Agent:",
    ["Calculator Agent", "Weather Agent", "Auto-Detect"]
)

# Display available tools
if st.session_state.calc_agent and st.session_state.weather_agent:
    st.sidebar.markdown("### Available Tools")
    
    st.sidebar.markdown("**🧮 Calculator Tools:**")
    for tool in st.session_state.calc_agent.tools:
        st.sidebar.markdown(f"- {tool.name}: {tool.description}")
    
    st.sidebar.markdown("**🌤️ Weather Tools:**")
    for tool in st.session_state.weather_agent.tools:
        st.sidebar.markdown(f"- {tool.name}: {tool.description}")

# Chat interface
user_input = st.chat_input("Ask me anything!")

if user_input:
    # Add user message to chat
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Determine which agent to use
    selected_agent = None
    agent_name = ""
    
    if agent_type == "Calculator Agent":
        selected_agent = st.session_state.calc_agent
        agent_name = "🧮 Calculator"
    elif agent_type == "Weather Agent":
        selected_agent = st.session_state.weather_agent
        agent_name = "🌤️ Weather"
    else:
        # Auto-detect based on keywords
        calc_keywords = ["add", "subtract", "multiply", "divide", "calculate", "math", "number", "sum", "product", "power"]
        weather_keywords = ["weather", "temperature", "forecast", "city", "climate", "hot", "cold", "rain", "sunny", "humidity"]
        
        user_lower = user_input.lower()
        calc_score = sum(1 for keyword in calc_keywords if keyword in user_lower)
        weather_score = sum(1 for keyword in weather_keywords if keyword in user_lower)
        
        if calc_score > weather_score:
            selected_agent = st.session_state.calc_agent
            agent_name = "🧮 Calculator"
        else:
            selected_agent = st.session_state.weather_agent
            agent_name = "🌤️ Weather"
    
    # Get agent response
    if selected_agent:
        with st.spinner(f"🤔 {agent_name} is thinking..."):
            try:
                # Use proper event loop handling for Windows
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                response = loop.run_until_complete(asyncio.wait_for(
                    selected_agent.ainvoke({
                        "input": user_input,
                        "chat_history": st.session_state.chat_history
                    }), 
                    timeout=60
                ))
                agent_response = response.get("output", str(response))
                st.session_state.chat_history.append({"role": "assistant", "content": f"[{agent_name}] {agent_response}"})
            except asyncio.TimeoutError:
                error_msg = "Request timed out. Please try again."
                st.session_state.chat_history.append({"role": "assistant", "content": f"[{agent_name}] {error_msg}"})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": f"[{agent_name}] {error_msg}"})
    else:
        st.session_state.chat_history.append({"role": "assistant", "content": "Agents not initialized. Please start the servers first."})

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Example queries
st.sidebar.markdown("### Example Queries")
st.sidebar.markdown("""
**Calculator:**
- What is 15 + 27?
- Multiply 8 and 12
- Calculate 5 to the power of 3

**Weather:**
- What's the weather in Tokyo?
- Get 3-day forecast for London
- Convert 25°C to Fahrenheit
- Weather alerts for New York
""")

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Reinitialize button
if st.sidebar.button("Reinitialize Agents"):
    st.session_state.calc_agent, st.session_state.weather_agent = initialize_agents()
    st.rerun()

# Debug info
if st.sidebar.checkbox("Show Debug Info"):
    st.sidebar.markdown("### Debug Information")
    st.sidebar.write(f"Calculator Agent: {st.session_state.calc_agent is not None}")
    st.sidebar.write(f"Weather Agent: {st.session_state.weather_agent is not None}")
    st.sidebar.write(f"Chat history length: {len(st.session_state.chat_history)}")
    st.sidebar.write(f"Platform: {sys.platform}") 