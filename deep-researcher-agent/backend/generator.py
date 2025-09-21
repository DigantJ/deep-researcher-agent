# generator.py

class Generator:
    def __init__(self):
        # Skip loading heavy Transformer model
        self.model = None

    def generate_answer(self, query, contexts):
        """
        Fallback generator:
        - Takes top 3 retrieved contexts
        - Returns them as a formatted answer
        - Defaults to a message if no contexts found
        """
        top_contexts = [ctx.get("text", "")
                        for ctx in contexts[:3] if ctx.get("text", "").strip()]

        if not top_contexts:
            return "No relevant information found."

        # Format as a simple numbered list
        formatted_answer = "\n".join(
            [f"{i+1}. {text}" for i, text in enumerate(top_contexts)])
        return formatted_answer


# Optional: testing snippet
if __name__ == "__main__":
    generator = Generator()
    sample_contexts = [
        {"text": "Context 1 about AI."},
        {"text": "Context 2 about Python."},
        {"text": "Context 3 about Transformers."},
    ]
    print(generator.generate_answer("Tell me something", sample_contexts))
