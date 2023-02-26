import os
from gpt_index import GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
os.environ["OPENAI_API_KEY"] = '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'


class IndexBot:
    def __init__(self, index_file_path):
        self.index = GPTSimpleVectorIndex.load_from_disk(index_file_path)
        self.max_input_size = 4096
        self.num_outputs = 256
        self.max_chunk_overlap = 20
        self.chunk_size_limit = 600
        self.prompt_helper = PromptHelper(
            self.max_input_size, self.num_outputs, self.max_chunk_overlap, chunk_size_limit=self.chunk_size_limit)
        self.llm_predictor = LLMPredictor(llm=OpenAI(
            temperature=0, model_name="text-ada-001", max_tokens=self.num_outputs))

    def ask_bot(self, query, history):
        # flattened_history = [item for sublist in history for item in sublist]
        # user_query = flattened_history + [query]
        # print(user_query)
        response = self.index.query(
            query, response_mode="compact")
        return response.response.strip()
