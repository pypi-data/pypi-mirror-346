from mcp import MCP, MCPRequest, MCPResponse
import uvicorn

app = MCP()

@app.route("/power")
async def calculate_power(request: MCPRequest) -> MCPResponse:
    try:
        data = request.json
        base = float(data.get("base", 0))
        exponent = float(data.get("exponent", 0))
        result = base ** exponent
        return MCPResponse.json({"result": result})
    except Exception as e:
        return MCPResponse.json({"error": str(e)}, status=400)

def run_server(host: str = "0.0.0.0", port: int = 8000):
    """启动MCP服务器
    
    Args:
        host (str): 服务器主机地址
        port (int): 服务器端口号
    """
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server() 