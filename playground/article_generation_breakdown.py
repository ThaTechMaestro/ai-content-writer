from typing import Any, Dict
from langchain.memory import ConversationBufferMemory




'''
This class Handles memory
'''
class OnlyStoreAIMemory(ConversationBufferMemory):
    
    '''
    Stores only model response in memory
    '''
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        input_str, output_str = self._get_input_output(inputs, outputs)
        self.chat_memory.add_ai_message(output_str)
