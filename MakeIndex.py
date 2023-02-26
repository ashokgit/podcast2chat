import os

from langchain import OpenAI
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
os.environ["OPENAI_API_KEY"] = 'Your Key here'


class MakeIndex:

    def __init__(self, directory_path, model_name='text-ada-001', max_tokens=256):
        self.directory_path = directory_path
        self.model_name = model_name
        self.max_tokens = max_tokens

    def construct_index(self):
        # set maximum input size
        max_input_size = 4096
        # set number of output tokens
        num_outputs = self.max_tokens
        # set maximum chunk overlap
        max_chunk_overlap = 20
        # set chunk size limit
        chunk_size_limit = 600

        prompt_helper = PromptHelper(
            max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

        # define LLM
        llm_predictor = LLMPredictor(llm=OpenAI(
            temperature=0, model_name=self.model_name, max_tokens=num_outputs))

        documents = SimpleDirectoryReader(self.directory_path).load_data()

        index = GPTSimpleVectorIndex(
            documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

        index.save_to_disk(self.directory_path+'/avatar.json')

        return index


print('Indexing...')
directory_path = 'transcriptions/AndrewHuberMan'
make_index = MakeIndex(directory_path)
index = make_index.construct_index()
print('Indexed!')
