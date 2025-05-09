from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BIANXIE_API_KEY")
api_base = os.getenv("BIANXIE_BASE")
Settings.llm = OpenAI(model="gpt-4o",api_key=api_key,api_base=api_base,temperature=0.1)
Settings.embed_model = OpenAIEmbedding(api_key=api_key,api_base =api_base)
Settings.text_splitter = SentenceSplitter(chunk_size=4096)


from .query import Queryr
from .build import KnowledgeBaseManager
