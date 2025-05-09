import asyncio
import json
from dataclasses import dataclass
from urllib.parse import urlparse

import click
import httpx
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.shared.exceptions import McpError
import mcp.server.stdio

LAW_RECOGNITION_API_BASE = "https://api-ailab.pkulaw.com/fabaoAI/tools/law_recognition"
MISSING_AUTH_TOKEN_MESSAGE = (
    """Legal Text token not found. Please specify your Legal Text token."""
)

class Law_recognitionError(Exception):
    pass
async def handle_law_recognition_text(
        http_client: httpx.AsyncClient, pkulaw_api_key: str, law_recognition_text: str
):
    try:
        #         law_recognition_text = extract_issue_id(law_recognition_text)

        response = await http_client.post(
            LAW_RECOGNITION_API_BASE, json={'text': law_recognition_text, "law_link": True},
            headers={"Authorization": f"Bearer {pkulaw_api_key}", 'Content-Type': 'application/json'}
        )
        if response.status_code == 401:
            raise McpError(
                "Error: Unauthorized. Please check your MCP_Pkulaw_Api_Key token."
            )
        response.raise_for_status()
        law_recognition_data = response.json()
        law_recognition_data_re = []
        for i in range(len(law_recognition_data)):
            law_recognition_data_dic = {}
            law_recognition_data_dic["text"] = law_recognition_data[i].get("text")
            law_recognition_data_dic["original"] = law_recognition_data[i].get("original")
            law_recognition_data_dic["fulltext"] = law_recognition_data[i].get("fulltext")
            law_recognition_data_dic["source"] = law_recognition_data[i].get("source")
            law_recognition_data_re.append(law_recognition_data_dic)
        return law_recognition_data_re

    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")

async def serve(pkulaw_api_key: str) -> Server:
    server = Server("law_recognition")
    http_client = httpx.AsyncClient()

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        return [
            types.Prompt(
                name="law_recognition_text",
                description="Extract and standardize the names of regulations and legal provisions",
                arguments=[
                    types.PromptArgument(
                        name="law_recognition_text",
                        description="Legal Text",
                        required=True,
                    )
                ],
            )
        ]


    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="get_law_recognition",
                description="""Identification and standardization of regulations and legal provisions. Use this tool when you need to:
                - Extract from the text paragraph: regulatory name and provisions
                - The extracted regulations and laws correspond to the names of standard regulations and the number of clauses in the regulatory database
                            """,
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Standardization of laws and regulations"
                        }
                    },
                    "required": ["text"]
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
            name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name != "get_law_recognition":
            raise ValueError(f"Unknown tool: {name}")

        if not arguments or "text" not in arguments:
            raise ValueError("Missing text argument")

        law_recognition_text_data = await handle_law_recognition_text(http_client, pkulaw_api_key, arguments["text"])
        # return law_recognition_text_data.to_tool_result()
        return [types.TextContent(type="text", text=json.dumps(law_recognition_text_data,ensure_ascii=False))]

    return server


@click.command()
@click.option(
    "--pkulaw_api_key",
    envvar="pkulaw_api_key",
    required=True,
    help="pkulaw_api_key",
)
def main(pkulaw_api_key: str):
    async def _run():
        print('1111111111111111')
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print('1111111111111111')
            server = await serve(pkulaw_api_key)
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="law_recognition",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_run())