from langchain.memory import ConversationBufferMemory


memory = ConversationBufferMemory()
memory.save_context({"input": "hi"}, {"output": "whats up"})
print(memory.load_memory_variables({}))