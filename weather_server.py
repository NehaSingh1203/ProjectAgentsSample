# weather_server.py
from fastmcp import FastMCP

mcp = FastMCP("WeatherServer")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather information for a city (static data)"""
    weather_data = {
        "New York": "🌤️ Sunny, 72°F (22°C), Humidity: 65%, Wind: 8 mph",
        "London": "🌧️ Rainy, 55°F (13°C), Humidity: 85%, Wind: 12 mph", 
        "Tokyo": "☁️ Cloudy, 68°F (20°C), Humidity: 70%, Wind: 5 mph",
        "Sydney": "☀️ Clear, 75°F (24°C), Humidity: 60%, Wind: 10 mph",
        "Paris": "⛅ Partly Cloudy, 62°F (17°C), Humidity: 75%, Wind: 6 mph",
        "Berlin": "🌦️ Light Rain, 58°F (14°C), Humidity: 80%, Wind: 9 mph",
        "Moscow": "❄️ Snow, 28°F (-2°C), Humidity: 70%, Wind: 15 mph",
        "Dubai": "☀️ Sunny, 88°F (31°C), Humidity: 45%, Wind: 3 mph",
        "Singapore": "🌧️ Thunderstorm, 82°F (28°C), Humidity: 90%, Wind: 7 mph",
        "Mumbai": "🌤️ Partly Sunny, 85°F (29°C), Humidity: 75%, Wind: 4 mph"
    }
    return weather_data.get(city, f"Weather data not available for {city}")

@mcp.tool()
def get_weather_forecast(city: str, days: int = 3) -> str:
    """Get weather forecast for a city for specified number of days (static data)"""
    forecasts = {
        "New York": {
            1: "🌤️ Day 1: Sunny, 72°F | 🌙 Night: Clear, 58°F",
            2: "⛅ Day 2: Partly Cloudy, 68°F | 🌙 Night: Cloudy, 55°F", 
            3: "🌧️ Day 3: Light Rain, 65°F | 🌙 Night: Rain, 52°F"
        },
        "London": {
            1: "🌧️ Day 1: Rain, 55°F | 🌙 Night: Heavy Rain, 48°F",
            2: "⛅ Day 2: Partly Cloudy, 58°F | 🌙 Night: Clear, 50°F",
            3: "🌤️ Day 3: Sunny, 62°F | 🌙 Night: Clear, 53°F"
        },
        "Tokyo": {
            1: "☁️ Day 1: Cloudy, 68°F | 🌙 Night: Overcast, 60°F",
            2: "🌧️ Day 2: Rain, 65°F | 🌙 Night: Rain, 58°F",
            3: "⛅ Day 3: Partly Cloudy, 70°F | 🌙 Night: Clear, 62°F"
        }
    }
    
    if city in forecasts:
        forecast = forecasts[city]
        result = f"Weather forecast for {city}:\n"
        for day in range(1, min(days + 1, 4)):
            if day in forecast:
                result += f"  {forecast[day]}\n"
        return result
    else:
        return f"Weather forecast not available for {city}"

@mcp.tool()
def get_temperature_conversion(celsius: float) -> str:
    """Convert Celsius to Fahrenheit"""
    fahrenheit = (celsius * 9/5) + 32
    return f"{celsius}°C = {fahrenheit:.1f}°F"

@mcp.tool()
def get_weather_alerts(city: str) -> str:
    """Get weather alerts for a city (static data)"""
    alerts = {
        "New York": "⚠️ No active weather alerts",
        "London": "⚠️ Flood warning in effect until tomorrow",
        "Tokyo": "⚠️ Typhoon warning - stay indoors",
        "Sydney": "⚠️ No active weather alerts",
        "Paris": "⚠️ High wind warning until evening"
    }
    return alerts.get(city, f"No weather alert data available for {city}")

if __name__ == "__main__":
    print("🌤️ Starting Weather MCP Server on http://localhost:8002")
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8002) 