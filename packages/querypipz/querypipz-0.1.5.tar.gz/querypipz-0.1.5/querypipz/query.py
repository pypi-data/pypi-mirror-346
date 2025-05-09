import os
import shutil
from llama_index.core import (
    load_index_from_storage,
    StorageContext,
)
from llama_index.core.indices.base import BaseIndex
from .queryengine import QueryType, QueryClass

class Queryr:
    def __init__(self, persist_dir: str):
        """
        Initialize the Queryr class with an index loaded from storage.

        Args:
            persist_dir (str): Directory where the index is persisted.
        """
        self.index: BaseIndex | None = None
        self._query_engine = None
        self._retriever = None

        if os.path.exists(persist_dir):
            try:
                storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
                self.index = load_index_from_storage(storage_context)
                print(f"Index loaded successfully from {persist_dir}.")
            except Exception as e:
                print(f"Error loading index from {persist_dir}: {e}")
                # Consider raising an exception or handling the error more robustly
        else:
            print(f"Index directory not found at {persist_dir}. Index will not be loaded.")

    def get_query_engine(self, similarity_top_k: int = 3, query_type: QueryType = QueryType.Query1):
        """
        Gets or initializes the query engine with specified parameters.

        Args:
            similarity_top_k (int): Number of top similar documents to retrieve. Defaults to 3.
            query_type (QueryType): Type of query to use. Defaults to QueryType.Query1.

        Returns:
            QueryClass: The initialized query engine.
        """
        if self.index is None:
            print("Index is not loaded. Cannot create query engine.")
            return None

        if self._query_engine is None:
            self._query_engine = QueryClass(
                querytype=query_type,
                index=self.index,
                similarity_top_k=similarity_top_k
            )
        return self._query_engine

    def get_retriever(self, similarity_top_k: int = 5):
        """
        Gets or sets up a retriever for fetching relevant documents without generating answers.

        Args:
            similarity_top_k (int): Number of top similar documents to retrieve. Defaults to 5.

        Returns:
            BaseRetriever: The initialized retriever.
        """
        if self.index is None:
            print("Index is not loaded. Cannot create retriever.")
            return None

        if self._retriever is None:
            self._retriever = self.index.as_retriever(similarity_top_k=similarity_top_k)
        return self._retriever

    def retrieve(self, query_text: str, similarity_top_k: int = 5):
        """
        Retrieve relevant documents based on the query text.

        Args:
            query_text (str): Text to search for relevant documents
            
        Returns:
            List[Document]: A list of retrieved documents.
        """
        retriever = self.get_retriever(similarity_top_k=similarity_top_k)
        if retriever:
            return retriever.retrieve(query_text)
        return []

    def query(self, prompt: str, similarity_top_k: int = 3, query_type: QueryType = QueryType.Query1):
        """
        Query the index with the given prompt and return the response.

        Args:
            prompt (str): The question to ask.
            similarity_top_k (int): Number of top similar documents to retrieve for the query engine. Defaults to 3.
            query_type (QueryType): Type of query to use. Defaults to QueryType.Query1.

        Returns:
            Response: The response from the query engine.
        """
        query_engine = self.get_query_engine(similarity_top_k=similarity_top_k, query_type=query_type)
        if query_engine:
            return query_engine.query(prompt)
        return "Index not loaded or query engine could not be initialized."

