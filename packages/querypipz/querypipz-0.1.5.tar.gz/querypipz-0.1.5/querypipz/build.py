import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from .reader import ReaderFactory, Reader
import shutil
from typing import List, Dict, Optional

class KnowledgeBaseManager:
    def __init__(self, base_persist_dir="./knowledge_bases"):
        self.base_persist_dir = base_persist_dir
        os.makedirs(self.base_persist_dir, exist_ok=True)
        self.indexes: Dict[str, VectorStoreIndex] = {}
        self._load_existing_indexes()

    def _load_existing_indexes(self):
        """Loads existing indexes from the base persist directory."""
        for kb_name in os.listdir(self.base_persist_dir):
            kb_path = os.path.join(self.base_persist_dir, kb_name)
            if os.path.isdir(kb_path):
                try:
                    storage_context = StorageContext.from_defaults(persist_dir=kb_path)
                    self.indexes[kb_name] = load_index_from_storage(storage_context)
                    print(f"Loaded knowledge base: {kb_name}")
                except Exception as e:
                    print(f"Could not load knowledge base {kb_name}: {e}")

    def build_or_update_kb(
        self,
        kb_name: str,
        file_paths: List[str],
        readertype=Reader.CustObsidianReader,
        debug=False,
    ):
        """
        Builds a new knowledge base or updates an existing one.

        Args:
            kb_name: The name of the knowledge base.
            file_paths: A list of directory paths to read documents from.
            readertype: The reader type to use for documents.
            debug: If True, limits the number of documents processed for debugging.
        """
        kb_persist_dir = os.path.join(self.base_persist_dir, kb_name)
        file_extractor = {".md": ReaderFactory(readertype)}

        all_documents = []
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"Warning: Directory not found: {file_path}")
                continue
            reader = SimpleDirectoryReader(
                input_dir=file_path,
                file_extractor=file_extractor,
                recursive=True,
            )
            all_documents.extend(reader.load_data())

        if debug:
            all_documents = all_documents[:10]

        if kb_name in self.indexes:
            # Update existing index (simplified: rebuild for now)
            print(f"Updating knowledge base: {kb_name}")
            # A more sophisticated approach would involve diffing documents and updating the index incrementally
            # For simplicity, we'll just rebuild the index for now.
            index = VectorStoreIndex.from_documents(all_documents)
            # Remove old index directory before persisting the new one
            if os.path.exists(kb_persist_dir):
                 shutil.rmtree(kb_persist_dir)
            index.storage_context.persist(persist_dir=kb_persist_dir)
            self.indexes[kb_name] = index
            print(f"Knowledge base '{kb_name}' updated with {len(all_documents)} documents.")
        else:
            # Build new index
            print(f"Building new knowledge base: {kb_name}")
            index = VectorStoreIndex.from_documents(all_documents)
            index.storage_context.persist(persist_dir=kb_persist_dir)
            self.indexes[kb_name] = index
            print(f"Knowledge base '{kb_name}' built with {len(all_documents)} documents.")

        return len(all_documents)

    def get_kb_index(self, kb_name: str) -> Optional[VectorStoreIndex]:
        """Retrieves a knowledge base index by name."""
        return self.indexes.get(kb_name)

    def list_kbs(self) -> List[str]:
        """Lists the names of available knowledge bases."""
        return list(self.indexes.keys())

    def delete_kb(self, kb_name: str):
        """Deletes a knowledge base."""
        if kb_name in self.indexes:
            kb_path = os.path.join(self.base_persist_dir, kb_name)
            if os.path.exists(kb_path):
                shutil.rmtree(kb_path)
                print(f"Deleted knowledge base directory: {kb_path}")
            del self.indexes[kb_name]
            print(f"Knowledge base '{kb_name}' deleted.")
        else:
            print(f"Knowledge base '{kb_name}' not found.")

