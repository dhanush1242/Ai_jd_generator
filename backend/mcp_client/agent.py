import asyncio
import os
import json
from dotenv import load_dotenv
from groq import Groq
from mcp.client import Client

load_dotenv()
MCP_SERVER_URL = "http://127.0.0.1:9000/mcp"
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def convert_mcp_tools_to_groq_tools(mcp_tools, role: str,):
    groq_tools = []
    candidate_tools = {"search_jobs_tool", "get_my_applications_tool", "get_application_status_tool",}
    recruiter_tools = {"get_recruiter_jobs_tool", "get_job_applications_tool", "get_application_notes_tool",}
    for tool in mcp_tools:
        if role == "candidate":
            if tool.name not in candidate_tools:
                continue
        elif role == "recruiter":
            if tool.name not in recruiter_tools:
                continue

        schema = tool.input_schema.copy()
        properties = schema.get("properties", {},).copy()
        required = schema.get("required", [],).copy()

        if role == "candidate": 
            properties.pop("candidate_id", None,)
            if "candidate_id" in required: required.remove("candidate_id")
        elif role == "recruiter":
            properties.pop("recruiter_id", None,)
            if "recruiter_id" in required: required.remove("recruiter_id")

        schema["properties"] = properties
        schema["required"] = required
        groq_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": (tool.description or ""),
                    "parameters": schema,
                },
            }
        )

    return groq_tools

def extract_tool_result(tool_result):
    if tool_result.structured_content is not None:
        return tool_result.structured_content
    texts = []
    for item in tool_result.content: 
        if hasattr(item, "text"): texts.append(item.text)
    return "\n".join(texts)

async def run_agent(user_message: str, role: str, user_id: int,) -> str:
    client = Client(MCP_SERVER_URL)
    async with client:
        result = await client.list_tools()
        groq_tools = convert_mcp_tools_to_groq_tools(result.tools, role,)
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are an AI Job Portal assistant. "
                    f"The authenticated user's role is {role}. "

                    "Use the available MCP tools whenever "
                    "job, application, or recruiter information "
                    "is required. "

                    "Only use information returned by the tools. "
                    "Do not invent job details, application details, "
                    "statuses, IDs, dates, or other information. "

                    "Never ask the user for their candidate ID "
                    "or recruiter ID because their identity is "
                    "already authenticated. "

                    "Do not claim that you can perform an action "
                    "unless an available MCP tool supports that action. "

                    "If no tool exists for applying, editing, publishing, "
                    "shortlisting, rejecting, or adding notes, explain "
                    "that the action is not currently available through "
                    "the chatbot."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages, # pyright: ignore[reportArgumentType]
            tools=groq_tools,
            tool_choice="auto",
        )
        assistant_message = response.choices[0].message
        if not assistant_message.tool_calls:
            return assistant_message.content or ""
        messages.append(assistant_message) # pyright: ignore[reportArgumentType]
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_arguments = json.loads(tool_call.function.arguments)
            if role == "candidate":
                if tool_name in {"get_my_applications_tool", "get_application_status_tool",}: tool_arguments["candidate_id"] = user_id
            elif role == "recruiter":
                if tool_name in {"get_recruiter_jobs_tool", "get_job_applications_tool", "get_application_notes_tool",}: tool_arguments["recruiter_id"] = user_id
            print("\nSelected MCP Tool:")
            print(tool_name)
            print("\nArguments after identity injection:")
            print(tool_arguments)
            tool_result = await client.call_tool(tool_name, tool_arguments,)
            print("\nMCP Result:")
            print(tool_result)
            tool_output = extract_tool_result(tool_result)
            if isinstance(tool_output, str):tool_content = tool_output
            else: tool_content = json.dumps(tool_output)

            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": tool_content,})

        final_response = groq_client.chat.completions.create(model="openai/gpt-oss-20b", messages=messages, tools=groq_tools,) # pyright: ignore[reportArgumentType]

        return (final_response.choices[0].message.content or "")

async def main():
    response = await run_agent(
        user_message=(
            "What is my application status "
            "for Python Developer?"),
        role="candidate",
        user_id=5,
    )
    print("\nAgent:")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())