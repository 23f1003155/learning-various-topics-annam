# client.py — MCP Client with Groq brain
import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from groq import Groq

import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL = "llama-3.3-70b-versatile"
SERVER_URL = "http://localhost:8000/mcp"

async def ask(user_message: str):
    try:
        async with streamablehttp_client(SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:

                await session.initialize()

                tools_response = await session.list_tools()
                groq_tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": t.name,
                            "description": t.description,
                            "parameters": t.inputSchema
                        }
                    }
                    for t in tools_response.tools
                ]

                print(f"\n{'═'*55}")
                print(f"👤 You asked       : {user_message}")
                print(f"🧰 Tools available : {[t.name for t in tools_response.tools]}")

                groq_client = Groq(api_key=GROQ_API_KEY)
                messages = [{"role": "user", "content": user_message}]

                response = groq_client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=groq_tools,
                    tool_choice="auto"
                )

                msg = response.choices[0].message

                if msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        fn_name = tool_call.function.name
                        fn_args = json.loads(tool_call.function.arguments)

                        print(f"🧠 Groq decided    : call '{fn_name}' with {fn_args}")

                        result = await session.call_tool(fn_name, fn_args)
                        tool_result = result.content[0].text
                        print(f"🔧 MCP tool result : {tool_result}")

                        messages.append({
                            "role": "assistant",
                            "tool_calls": [tool_call.model_dump()]
                        })
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result
                        })

                    final = groq_client.chat.completions.create(
                        model=MODEL,
                        messages=messages
                    )
                    print(f"🤖 Final answer    : {final.choices[0].message.content}")

                else:
                    print(f"🤖 Direct answer   : {msg.content}")

                print(f"{'═'*55}\n")

    except ConnectionRefusedError:
        print(f"\n❌ Server not running! Open new terminal and run: python server.py\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


async def main():
    await ask("What is today's date and time?")
    await ask("Convert 200 USD to INR")

asyncio.run(main())