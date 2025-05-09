# Project description
Identification and standardization of regulations and legal provisions. Use this tool when you need to:
- Extract from the text paragraph: regulatory name and provisions
- The extracted regulations and laws correspond to the names of standard regulations and the number of clauses in the regulatory database
# Requirements
- requires-python = ">=3.10"
- mcp>=1.0.0
# Installation
- pip install mcp_server_law_recognition
# Usage
## Sample
    from mcp import ClientSession, StdioServerParameters, types
    from mcp.client.stdio import stdio_client
    server_params = StdioServerParameters(
        command="python",  # Executable
        args=["-m","mcp_server_law_recognition"],  # Optional command line arguments
        env={
            "pkulaw_api_key": "da9629867ee841518***********"
        }  # Optional environment variables
    ) 
     
    async def run():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(
                read, write
            ) as session:
                # Initialize the connection
                await session.initialize()

            tools = await session.list_tools()
            print('tools:',tools)
            result = await session.call_tool("get_law_recognition", arguments={"text": "根据《民法典》第一千二百六十条规定，该法自2021年1月1日起施行，同时废止了《中华人民共和国婚姻法》、《中华人民共和国继承法》、《中华人民共和国民法通则》..."})
            print('result:',result)

    if __name__ == "__main__":
        import asyncio
    
        asyncio.run(run())
# Contact US
- Apply for an APIKEY:lifajie@chinalawinfo.com