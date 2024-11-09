class ContextManager:
    """Manages context selection and ranking"""
    
    def __init__(self, max_contexts: int = 3):
        self.max_contexts = max_contexts