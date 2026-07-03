import json

from openai import OpenAI

from .models import ChatMessage, LlmAgent
from .tools.registry import execute_tool, get_openai_tools, reload_registry

MAX_TOOL_ITERATIONS = 10


class LlmAgentService:
    @staticmethod
    def build_client(agent: LlmAgent) -> OpenAI:
        if agent.use_other_agent:
            return OpenAI(base_url=agent.base_url, api_key=agent.api_key)
        return OpenAI(api_key=agent.api_key)

    @staticmethod
    def build_system_message(agent: LlmAgent) -> str:
        system_content = agent.role.strip()
        if agent.context.strip():
            system_content = f"{system_content}\n\n{agent.context.strip()}"
        return system_content

    @classmethod
    def get_agent_tool_names(cls, agent: LlmAgent) -> list[str]:
        return list(
            agent.tools.filter(active=True, file_generated=True).values_list("name", flat=True)
        )

    @classmethod
    def build_openai_tools(cls, agent: LlmAgent) -> list[dict]:
        tool_names = cls.get_agent_tool_names(agent)
        if not tool_names:
            return []
        reload_registry()
        return get_openai_tools(tool_names)

    @classmethod
    def build_messages(
        cls,
        agent: LlmAgent,
        prompt: str,
        event_id: str,
    ) -> list[dict]:
        messages: list[dict] = [
            {"role": "system", "content": cls.build_system_message(agent)}
        ]

        history = ChatMessage.objects.filter(
            event_id=event_id,
            agent=agent,
        ).order_by("created_at")

        for message in history:
            messages.append({"role": message.role, "content": message.content})

        messages.append({"role": "user", "content": prompt})
        return messages

    @classmethod
    def _message_to_dict(cls, message) -> dict:
        data = {
            "role": message.role,
            "content": message.content or "",
        }
        if message.tool_calls:
            data["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in message.tool_calls
            ]
        return data

    @classmethod
    def _complete_with_tools(
        cls,
        client: OpenAI,
        agent: LlmAgent,
        messages: list[dict],
    ) -> str:
        tools = cls.build_openai_tools(agent)
        kwargs: dict = {
            "model": agent.model.name,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        for _ in range(MAX_TOOL_ITERATIONS):
            response = client.chat.completions.create(**kwargs)
            message = response.choices[0].message

            if not message.tool_calls:
                return message.content or ""

            messages.append(cls._message_to_dict(message))

            for tool_call in message.tool_calls:
                arguments = json.loads(tool_call.function.arguments or "{}")
                result = execute_tool(tool_call.function.name, arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

        return "Error: tool loop exceeded maximum iterations."

    @classmethod
    def run(cls, agent: LlmAgent, prompt: str, event_id: str) -> str:
        client = cls.build_client(agent)
        messages = cls.build_messages(agent, prompt, event_id)
        content = cls._complete_with_tools(client, agent, messages)
        cls._save_exchange(agent, event_id, prompt, content)
        return content

    @classmethod
    def run_stream(cls, agent: LlmAgent, prompt: str, event_id: str):
        client = cls.build_client(agent)
        messages = cls.build_messages(agent, prompt, event_id)
        content = cls._complete_with_tools(client, agent, messages)

        chunk_size = 24
        for index in range(0, len(content), chunk_size):
            yield content[index : index + chunk_size]

        cls._save_exchange(agent, event_id, prompt, content)

    @staticmethod
    def _save_exchange(
        agent: LlmAgent,
        event_id: str,
        prompt: str,
        content: str,
    ) -> None:
        ChatMessage.objects.create(
            event_id=event_id,
            agent=agent,
            role=ChatMessage.Role.USER,
            content=prompt,
        )
        ChatMessage.objects.create(
            event_id=event_id,
            agent=agent,
            role=ChatMessage.Role.ASSISTANT,
            content=content,
        )
