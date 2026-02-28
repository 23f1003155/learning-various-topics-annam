import asyncio
import json
import re
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from groq import Groq



MODEL = "llama-3.3-70b-versatile"
groq_client = Groq()
#while using we need to create key and add that inside () above.

def is_math_question(text: str) -> bool:
    return bool(re.search(r"\b(add|plus|minus|subtract|multiply|times|\+|\-|\*)\b", text.lower()))

async def ask(user_message: str):

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
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

            messages = [{"role": "user", "content": user_message}]

            # ✅ ONLY enable tools for math
            if is_math_question(user_message):
                response = groq_client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=groq_tools,
                    tool_choice="auto"
                )
            else:
                response = groq_client.chat.completions.create(
                    model=MODEL,
                    messages=messages
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


async def main():
    await ask("What is 5 plus 7?")
    await ask("What is 4 multiplied by 6?")
    await ask("What is 10 minus 3?")
    await ask("What is the capital of India?")

asyncio.run(main())
