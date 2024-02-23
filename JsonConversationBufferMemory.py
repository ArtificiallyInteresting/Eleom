import json
from typing import Any, Dict
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage

class JsonConversationBufferMemory(ConversationBufferMemory):
    def __init__(self):
        super().__init__()
        self.output_key = "response"
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        input_str, output_str = self._get_input_output(inputs, outputs)
        output_str = json.loads(output_str.strip())[self.output_key]
        self.chat_memory.add_messages(
            [HumanMessage(content=input_str), AIMessage(content=output_str)]
        )

    async def asave_context(
        self, inputs: Dict[str, Any], outputs: Dict[str, str]
    ) -> None:
        """Save context from this conversation to buffer."""
        input_str, output_str = self._get_input_output(inputs, outputs)
        output_str = json.loads(output_str)[self.output_key]
        await self.chat_memory.aadd_messages(
            [HumanMessage(content=input_str), AIMessage(content=output_str)]
        )